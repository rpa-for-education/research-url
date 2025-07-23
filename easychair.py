import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# URL của trang EasyChair và API
SOURCE_URL = 'https://easychair.org/cfp/'
API_URL = 'https://api.rpa4edu.shop/api_research.php'
HEADERS = {'Content-Type': 'application/json'}

def parse_date(date_str):
    """Chuyển đổi định dạng ngày từ 'MMM DD, YYYY' sang 'YYYY-MM-DD'"""
    try:
        return datetime.strptime(date_str, '%b %d, %Y').strftime('%Y-%m-%d')
    except ValueError:
        return date_str  # Giữ nguyên nếu không parse được

print("🚀 Bắt đầu cào dữ liệu...")
response = requests.get(SOURCE_URL, timeout=10)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')
rows = soup.select('table tbody tr')
print(f"Tìm thấy {len(rows)} hàng để xử lý.\n")

data = []
base_url = 'https://easychair.org'

# Thu thập dữ liệu từ trang EasyChair
for i, row in enumerate(rows, start=1):
    try:
        print(f"🔹 Hàng {i}/{len(rows)}...", end="\r")
        cols = row.find_all('td')
        if len(cols) >= 6:
            acronym = cols[0].text.strip()
            name = cols[1].text.strip()
            location = cols[2].text.strip()
            deadline = parse_date(cols[3].text.strip())
            start_date = parse_date(cols[4].text.strip())
            topics = [e.text.strip() for e in cols[5].find_all('span', class_='badge')]
            url_link = cols[0].find('a', href=True)
            conf_url = url_link['href'] if url_link else ''
            if conf_url and not conf_url.startswith('http'):
                conf_url = base_url + conf_url
            data.append({
                'acronym': acronym,
                'name': name,
                'location': location,
                'deadline': deadline,
                'start_date': start_date,
                'topics': ", ".join(topics),
                'url': conf_url
            })
    except Exception as e:
        print(f"\n⚠️ Lỗi tại hàng {i}: {e}")

# Kiểm tra dữ liệu hiện có bằng GET
print("\n📡 Kiểm tra dữ liệu hiện có trong cơ sở dữ liệu...")
existing_conferences = {}
try:
    response = requests.get(API_URL, headers=HEADERS, timeout=10)
    if response.status_code == 200:
        try:
            existing_data = response.json()
            for conf in existing_data:
                key = (conf['acronym'], conf['start_date'])
                existing_conferences[key] = conf['id_conference']
            print(f"✅ Tìm thấy {len(existing_conferences)} hội thảo trong cơ sở dữ liệu.")
        except ValueError:
            print(f"⚠️ Phản hồi GET không phải JSON: {response.text}")
    else:
        print(f"⚠️ Lỗi GET {response.status_code}: {response.text}")
except Exception as e:
    print(f"⚠️ Lỗi khi gửi yêu cầu GET: {e}")

# Phân loại bản ghi: thêm mới (POST) hoặc cập nhật (PUT)
records_to_post = []
records_to_put = []
for record in data:
    key = (record['acronym'], record['start_date'])
    if key in existing_conferences:
        record['id_conference'] = existing_conferences[key]
        records_to_put.append(record)
    else:
        records_to_post.append(record)

# Gửi dữ liệu mới qua POST
success_count = 0
batch_size = 50

if records_to_post:
    print("\n📤 Gửi dữ liệu mới đến API (POST)...")
    for i in range(0, len(records_to_post), batch_size):
        batch = records_to_post[i:i + batch_size]
        try:
            response = requests.post(API_URL, json=batch, headers=HEADERS, timeout=10)
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    for j, result in enumerate(response_data.get('results', [])):
                        record = batch[j]
                        if result.get('message') == "Thêm hội thảo thành công":
                            success_count += 1
                            print(f"  🔹 Bản ghi {i + j + 1}/{len(data)} - {record['acronym']}: Thêm thành công. ID: {result.get('id_conference')}")
                        elif result.get('message') == "Hội thảo đã tồn tại":
                            print(f"  🔹 Bản ghi {i + j + 1}/{len(data)} - {record['acronym']}: Đã tồn tại. ID: {result.get('id_conference')}")
                            record['id_conference'] = result.get('id_conference')
                            records_to_put.append(record)
                        else:
                            print(f"  🔹 Bản ghi {i + j + 1}/{len(data)} - {record['acronym']}: Lỗi: {result.get('error')}")
                    print(f"✅ Lô {i//batch_size + 1} ({len(batch)} bản ghi): Xử lý thành công.")
                except ValueError:
                    print(f"  ⚠️ Phản hồi API không phải JSON: {response.text}")
            else:
                print(f"❌ Lô {i//batch_size + 1} ({len(batch)} bản ghi): Lỗi {response.status_code} - {response.text}")
                for j, record in enumerate(batch):
                    print(f"  🔹 Bản ghi {i + j + 1}/{len(data)} - {record['acronym']}: Thất bại.")
        except Exception as e:
            print(f"❌ Lô {i//batch_size + 1} ({len(batch)} bản ghi): Lỗi khi gửi: {e}")
            for j, record in enumerate(batch):
                print(f"  🔹 Bản ghi {i + j + 1}/{len(data)} - {record['acronym']}: Thất bại.")

# Gửi dữ liệu cập nhật qua PUT
if records_to_put:
    print("\n📤 Gửi dữ liệu cập nhật đến API (PUT)...")
    for i in range(0, len(records_to_put), batch_size):
        batch = records_to_put[i:i + batch_size]
        try:
            response = requests.put(API_URL, json=batch, headers=HEADERS, timeout=10)
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    for j, result in enumerate(response_data.get('results', [])):
                        record = batch[j]
                        if result.get('message') == "Cập nhật hội thảo thành công":
                            success_count += 1
                            print(f"  🔹 Bản ghi {i + j + 1}/{len(records_to_put)} - {record['acronym']}: Cập nhật thành công.")
                        else:
                            print(f"  🔹 Bản ghi {i + j + 1}/{len(records_to_put)} - {record['acronym']}: Lỗi: {result.get('error')}")
                    print(f"✅ Lô {i//batch_size + 1} ({len(batch)} bản ghi): Cập nhật thành công.")
                except ValueError:
                    print(f"  ⚠️ Phản hồi API không phải JSON: {response.text}")
            else:
                print(f"❌ Lô {i//batch_size + 1} ({len(batch)} bản ghi): Lỗi {response.status_code} - {response.text}")
                for j, record in enumerate(batch):
                    print(f"  🔹 Bản ghi {i + j + 1}/{len(records_to_put)} - {record['acronym']}: Thất bại.")
        except Exception as e:
            print(f"❌ Lô {i//batch_size + 1} ({len(batch)} bản ghi): Lỗi khi gửi: {e}")
            for j, record in enumerate(batch):
                print(f"  🔹 Bản ghi {i + j + 1}/{len(records_to_put)} - {record['acronym']}: Thất bại.")

# (Tùy chọn) Xóa hội thảo nếu cần
# records_to_delete = [{'id_conference': 1, 'acronym': 'ICML2025'}, ...]  # Thay bằng danh sách ID cần xóa
records_to_delete = []  # Để trống nếu không muốn xóa
if records_to_delete:
    print("\n📤 Gửi yêu cầu xóa đến API (DELETE)...")
    for i in range(0, len(records_to_delete), batch_size):
        batch = records_to_delete[i:i + batch_size]
        try:
            response = requests.delete(API_URL, json=batch, headers=HEADERS, timeout=10)
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    for j, result in enumerate(response_data.get('results', [])):
                        record = batch[j]
                        if result.get('message') == "Xóa hội thảo thành công":
                            success_count += 1
                            print(f"  🔹 Bản ghi {i + j + 1}/{len(records_to_delete)} - {record['acronym']}: Xóa thành công.")
                        else:
                            print(f"  🔹 Bản ghi {i + j + 1}/{len(records_to_delete)} - {record['acronym']}: Lỗi: {result.get('error')}")
                    print(f"✅ Lô {i//batch_size + 1} ({len(batch)} bản ghi): Xóa thành công.")
                except ValueError:
                    print(f"  ⚠️ Phản hồi API không phải JSON: {response.text}")
            else:
                print(f"❌ Lô {i//batch_size + 1} ({len(batch)} bản ghi): Lỗi {response.status_code} - {response.text}")
                for j, record in enumerate(batch):
                    print(f"  🔹 Bản ghi {i + j + 1}/{len(records_to_delete)} - {record['acronym']}: Thất bại.")
        except Exception as e:
            print(f"❌ Lô {i//batch_size + 1} ({len(batch)} bản ghi): Lỗi khi gửi: {e}")
            for j, record in enumerate(batch):
                print(f"  🔹 Bản ghi {i + j + 1}/{len(records_to_delete)} - {record['acronym']}: Thất bại.")

print(f"\n🏁 Hoàn tất! Đã xử lý thành công {success_count}/{len(data)} bản ghi.")