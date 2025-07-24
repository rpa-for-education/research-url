import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# Danh sách URL cần quét
URLS = [
    'https://easychair.org/cfp/',
    'https://easychair.org/cfp/random.cgi',
    'https://easychair.org/cfp/area.cgi?area=6',
    'https://easychair.org/cfp/area.cgi?area=15',
    'https://easychair.org/cfp/area.cgi?area=13',
    'https://easychair.org/cfp/area.cgi?area=18',
    'https://easychair.org/cfp/area.cgi?area=19',
    'https://easychair.org/cfp/area.cgi?area=8',
    'https://easychair.org/cfp/area.cgi?area=16',
    'https://easychair.org/cfp/area.cgi?area=10',
    'https://easychair.org/cfp/area.cgi?area=24',
    'https://easychair.org/cfp/area.cgi?area=11',
    'https://easychair.org/cfp/area.cgi?area=1',
    'https://easychair.org/cfp/area.cgi?area=17',
    'https://easychair.org/cfp/area.cgi?area=7',
    'https://easychair.org/cfp/area.cgi?area=4',
    'https://easychair.org/cfp/area.cgi?area=5',
    'https://easychair.org/cfp/area.cgi?area=12',
    'https://easychair.org/cfp/area.cgi?area=2',
    'https://easychair.org/cfp/area.cgi?area=14',
    'https://easychair.org/cfp/area.cgi?area=9',
    'https://easychair.org/cfp/topic.cgi?tid=670',
    'https://easychair.org/cfp/topic.cgi?tid=401',
    'https://easychair.org/cfp/topic.cgi?tid=752',
    'https://easychair.org/cfp/topic.cgi?tid=26492',
    'https://easychair.org/cfp/topic.cgi?tid=16901',
    'https://easychair.org/cfp/topic.cgi?tid=27052',
    'https://easychair.org/cfp/topic.cgi?tid=16993',
    'https://easychair.org/cfp/topic.cgi?tid=18115',
    'https://easychair.org/cfp/topic.cgi?tid=49240',
    'https://easychair.org/cfp/topic.cgi?tid=3221',
    'https://easychair.org/cfp/topic.cgi?tid=27610129',
    'https://easychair.org/cfp/topic.cgi?tid=565064',
    'https://easychair.org/cfp/topic.cgi?tid=65909',
    'https://easychair.org/cfp/topic.cgi?tid=6766858',
    'https://easychair.org/cfp/topic.cgi?tid=1763',
    'https://easychair.org/cfp/topic.cgi?tid=5691',
    'https://easychair.org/cfp/topic.cgi?tid=10330',
    'https://easychair.org/cfp/topic.cgi?tid=72495',
    'https://easychair.org/cfp/topic.cgi?tid=84867',
    'https://easychair.org/cfp/topic.cgi?tid=39582319',
    'https://easychair.org/cfp/topic.cgi?tid=3258657',
    'https://easychair.org/cfp/topic.cgi?tid=753432',
    'https://easychair.org/cfp/topic.cgi?tid=37801319',
    'https://easychair.org/cfp/topic.cgi?tid=67784',
    'https://easychair.org/cfp/country.cgi?cc=vn',
    'https://easychair.org/cfp/country.cgi?cc=cn',
    'https://easychair.org/cfp/country.cgi?cc=us',
    'https://easychair.org/cfp/country.cgi?cc=it',
    'https://easychair.org/cfp/country.cgi?cc=in',
    'https://easychair.org/cfp/country.cgi?cc=de',
    'https://easychair.org/cfp/country.cgi?cc=jp',
    'https://easychair.org/cfp/country.cgi?cc=gb',
    'https://easychair.org/cfp/country.cgi?cc=fr',
    'https://easychair.org/cfp/country.cgi?cc=ca',
    'https://easychair.org/cfp/country.cgi?cc=es',
    'https://easychair.org/cfp/country.cgi?cc=au',
    'https://easychair.org/cfp/country.cgi?cc=kh',
    'https://easychair.org/cfp/country.cgi?cc=hr',
    'https://easychair.org/cfp/country.cgi?cc=es',
    'https://easychair.org/cfp/country.cgi?cc=fi',
    'https://easychair.org/cfp/country.cgi?cc=hk',
    'https://easychair.org/cfp/country.cgi?cc=is',
    'https://easychair.org/cfp/country.cgi?cc=id',
    'https://easychair.org/cfp/country.cgi?cc=ie',
    'https://easychair.org/cfp/country.cgi?cc=is',
    'https://easychair.org/cfp/country.cgi?cc=jo',
    'https://easychair.org/cfp/country.cgi?cc=al',
    'https://easychair.org/cfp/country.cgi?cc=dz',
    'https://easychair.org/cfp/country.cgi?cc=ao',
    'https://easychair.org/cfp/country.cgi?cc=ar',
    'https://easychair.org/cfp/country.cgi?cc=am',
    'https://easychair.org/cfp/country.cgi?cc=ar',
    'https://easychair.org/cfp/country.cgi?cc=at',
    'https://easychair.org/cfp/country.cgi?cc=az',
    'https://easychair.org/cfp/country.cgi?cc=bh',
    'https://easychair.org/cfp/country.cgi?cc=bd',
    'https://easychair.org/cfp/country.cgi?cc=be',
    'https://easychair.org/cfp/country.cgi?cc=bj',
    'https://easychair.org/cfp/country.cgi?cc=bt',
    'https://easychair.org/cfp/country.cgi?cc=ba',
    'https://easychair.org/cfp/country.cgi?cc=bw',
    'https://easychair.org/cfp/country.cgi?cc=br',
    'https://easychair.org/cfp/country.cgi?cc=bn',
    'https://easychair.org/cfp/country.cgi?cc=bg',
    'https://easychair.org/cfp/country.cgi?cc=bf',
    'https://easychair.org/cfp/country.cgi?cc=cl',
    'https://easychair.org/cfp/country.cgi?cc=co',
    'https://easychair.org/cfp/country.cgi?cc=cy',
    'https://easychair.org/cfp/country.cgi?cc=cz',
    'https://easychair.org/cfp/country.cgi?cc=dk',
    'https://easychair.org/cfp/country.cgi?cc=ec',
    'https://easychair.org/cfp/country.cgi?cc=eg',
    'https://easychair.org/cfp/country.cgi?cc=ee',
    'https://easychair.org/cfp/country.cgi?cc=ge',
    'https://easychair.org/cfp/country.cgi?cc=gr',
    'https://easychair.org/cfp/country.cgi?cc=hn',
    'https://easychair.org/cfp/country.cgi?cc=hu',
    'https://easychair.org/cfp/country.cgi?cc=ir',
    'https://easychair.org/cfp/country.cgi?cc=iq',
    'https://easychair.org/cfp/country.cgi?cc=il',
    'https://easychair.org/cfp/country.cgi?cc=ke',
    'https://easychair.org/cfp/country.cgi?cc=kg',
    'https://easychair.org/cfp/country.cgi?cc=lv',
    'https://easychair.org/cfp/country.cgi?cc=lt',
    'https://easychair.org/cfp/country.cgi?cc=lu',
    'https://easychair.org/cfp/country.cgi?cc=mk',
    'https://easychair.org/cfp/country.cgi?cc=my',
    'https://easychair.org/cfp/country.cgi?cc=mr',
    'https://easychair.org/cfp/country.cgi?cc=mu',
    'https://easychair.org/cfp/country.cgi?cc=mx',
    'https://easychair.org/cfp/country.cgi?cc=mn',
    'https://easychair.org/cfp/country.cgi?cc=me',
    'https://easychair.org/cfp/country.cgi?cc=ma',
    'https://easychair.org/cfp/country.cgi?cc=np',
    'https://easychair.org/cfp/country.cgi?cc=nl',
    'https://easychair.org/cfp/country.cgi?cc=nz',
    'https://easychair.org/cfp/country.cgi?cc=ng',
    'https://easychair.org/cfp/country.cgi?cc=no',
    'https://easychair.org/cfp/country.cgi?cc=om',
    'https://easychair.org/cfp/country.cgi?cc=pk',
    'https://easychair.org/cfp/country.cgi?cc=pa',
    'https://easychair.org/cfp/country.cgi?cc=pe',
    'https://easychair.org/cfp/country.cgi?cc=ph',
    'https://easychair.org/cfp/country.cgi?cc=pl',
    'https://easychair.org/cfp/country.cgi?cc=pt',
    'https://easychair.org/cfp/country.cgi?cc=qa',
    'https://easychair.org/cfp/country.cgi?cc=ro',
    'https://easychair.org/cfp/country.cgi?cc=ru',
    'https://easychair.org/cfp/country.cgi?cc=rw',
    'https://easychair.org/cfp/country.cgi?cc=sm',
    'https://easychair.org/cfp/country.cgi?cc=sa',
    'https://easychair.org/cfp/country.cgi?cc=rs',
    'https://easychair.org/cfp/country.cgi?cc=sg',
    'https://easychair.org/cfp/country.cgi?cc=si',
    'https://easychair.org/cfp/country.cgi?cc=ra',
    'https://easychair.org/cfp/country.cgi?cc=kz',
    'https://easychair.org/cfp/country.cgi?cc=lk',
    'https://easychair.org/cfp/country.cgi?cc=se',
    'https://easychair.org/cfp/country.cgi?cc=ch',
    'https://easychair.org/cfp/country.cgi?cc=tw',
    'https://easychair.org/cfp/country.cgi?cc=tz',
    'https://easychair.org/cfp/country.cgi?cc=th',
    'https://easychair.org/cfp/country.cgi?cc=tn',
    'https://easychair.org/cfp/country.cgi?cc=tz',
    'https://easychair.org/cfp/country.cgi?cc=ug',
    'https://easychair.org/cfp/country.cgi?cc=ua',
    'https://easychair.org/cfp/country.cgi?cc=ae',
    'https://easychair.org/cfp/country.cgi?cc=uy',
    'https://easychair.org/cfp/country.cgi?cc=uz',
    'https://easychair.org/cfp/country.cgi?cc=ye',
    'https://easychair.org/cfp/country.cgi?cc=zw'
]

# API và headers
API_URL = 'https://api.rpa4edu.shop/api_research.php'
HEADERS = {'Content-Type': 'application/json'}

def parse_date(date_str):
    """Chuyển đổi định dạng ngày từ 'MMM DD, YYYY' sang 'YYYY-MM-DD'"""
    try:
        return datetime.strptime(date_str, '%b %d, %Y').strftime('%Y-%m-%d')
    except ValueError:
        return date_str  # Giữ nguyên nếu không parse được

def get_current_time():
    """Lấy thời gian hiện tại định dạng YYYY-MM-DD HH:MM:SS"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def scrape_url(url):
    """Quét dữ liệu từ một URL EasyChair"""
    print(f"🚀 Quét dữ liệu từ {url}...")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.select('table tbody tr')
        print(f"Tìm thấy {len(rows)} hàng tại {url}.")

        data = []
        base_url = 'https://easychair.org'

        for i, row in enumerate(rows, start=1):
            try:
                print(f"🔹 Hàng {i}/{len(rows)} tại {url}...", end="\r")
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
                print(f"\n⚠️ Lỗi tại hàng {i} của {url}: {e}")
        return data
    except Exception as e:
        print(f"\n⚠️ Lỗi khi quét {url}: {e}")
        return []

# Thu thập dữ liệu từ tất cả URL và loại bỏ trùng lặp
print("🚀 Bắt đầu cào dữ liệu từ tất cả URL...")
all_data = []
seen = set()  # Lưu trữ các bản ghi đã thấy để loại bỏ trùng lặp
for url in URLS:
    data = scrape_url(url)
    for record in data:
        key = (record['acronym'], record['start_date'])
        if key not in seen:
            seen.add(key)
            all_data.append(record)
print(f"\n✅ Thu thập được {len(all_data)} bản ghi duy nhất.")

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
current_time = get_current_time()
for record in all_data:
    key = (record['acronym'], record['start_date'])
    if key in existing_conferences:
        record['id_conference'] = existing_conferences[key]
        record['modified_time'] = current_time  # Thêm modified_time cho PUT
        records_to_put.append(record)
    else:
        record['created_time'] = current_time  # Thêm created_time cho POST
        record['modified_time'] = current_time  # Thêm modified_time cho POST
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
                            print(f"  🔹 Bản ghi {i + j + 1}/{len(all_data)} - {record['acronym']}: Thêm thành công. ID: {result.get('id_conference')}")
                        elif result.get('message') == "Hội thảo đã tồn tại":
                            print(f"  🔹 Bản ghi {i + j + 1}/{len(all_data)} - {record['acronym']}: Đã tồn tại. ID: {result.get('id_conference')}")
                            record['id_conference'] = result.get('id_conference')
                            record['modified_time'] = current_time
                            records_to_put.append(record)
                        else:
                            print(f"  🔹 Bản ghi {i + j + 1}/{len(all_data)} - {record['acronym']}: Lỗi: {result.get('error')}")
                    print(f"✅ Lô {i//batch_size + 1} ({len(batch)} bản ghi): Xử lý thành công.")
                except ValueError:
                    print(f"  ⚠️ Phản hồi API không phải JSON: {response.text}")
            else:
                print(f"❌ Lô {i//batch_size + 1} ({len(batch)} bản ghi): Lỗi {response.status_code} - {response.text}")
                for j, record in enumerate(batch):
                    print(f"  🔹 Bản ghi {i + j + 1}/{len(all_data)} - {record['acronym']}: Thất bại.")
        except Exception as e:
            print(f"❌ Lô {i//batch_size + 1} ({len(batch)} bản ghi): Lỗi khi gửi: {e}")
            for j, record in enumerate(batch):
                print(f"  🔹 Bản ghi {i + j + 1}/{len(all_data)} - {record['acronym']}: Thất bại.")

# Gửi dữ liệu cập nhật qua PUT
if records_to_put:
    print("\n📤 Gửi dữ liệu cập nhật đến API (PUT)...")
    for i in range(0, len(records_to_put), batch_size):
        batch = records_to_put[i:i + batch_size]
        # Loại bỏ created_time khỏi payload PUT để tránh ghi đè
        batch_for_put = [
            {k: v for k, v in record.items() if k != 'created_time'}
            for record in batch
        ]
        try:
            response = requests.put(API_URL, json=batch_for_put, headers=HEADERS, timeout=10)
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

# Xử lý xóa (nếu có)
records_to_delete = []  # Để trống theo yêu cầu
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

print(f"\n🏁 Hoàn tất! Đã xử lý thành công {success_count}/{len(all_data)} bản ghi.")