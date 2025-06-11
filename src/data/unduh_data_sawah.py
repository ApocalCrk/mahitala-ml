# File: unduh_data_sawah.py (Versi Final dengan Parser Esri JSON)
import requests
import geopandas as gpd
from shapely.geometry import Polygon
import warnings
from urllib3.exceptions import InsecureRequestWarning

# Menyembunyikan pesan warning SSL
warnings.filterwarnings('ignore', category=InsecureRequestWarning)

def parse_and_download_sawah_data(provinsi_target="DAERAH ISTIMEWA YOGYAKARTA"):
    """
    Fungsi untuk mengunduh dan mem-parsing data poligon lahan sawah
    dari ArcGIS Feature Service (format Esri JSON).
    """
    query_url = "https://kspservices.big.go.id/satupeta/rest/services/PUBLIK/SUMBER_DAYA_ALAM_DAN_LINGKUNGAN/MapServer/36/query"

    params = {
        'where': '1=1', # Ambil semua data terlebih dahulu
        'outFields': '*',
        'outSR': '4326',
        'f': 'json', # Minta format json standar dari Esri
        'resultOffset': 0,
        'resultRecordCount': 2000
    }
    
    print(f"Mulai mengunduh data lahan sawah dari server BIG...")
    
    all_features = []
    
    while True:
        try:
            print(f"Mengambil data dari offset: {params['resultOffset']}...")
            response = requests.get(query_url, params=params, timeout=90, verify=False)
            response.raise_for_status()
            data = response.json()
            
            if 'error' in data:
                print(f"Server memberikan error: {data['error']}")
                return None

            features = data.get('features', [])
            
            if features:
                all_features.extend(features)
                # Cek apakah ini halaman terakhir (logika untuk server Esri)
                if 'exceededTransferLimit' not in data or data['exceededTransferLimit'] is False:
                    print("Pengambilan data dari server selesai (halaman terakhir).")
                    break
                else:
                    # Pindah ke halaman berikutnya
                    params['resultOffset'] += len(features)
            else:
                print("Tidak ada lagi data yang ditemukan. Pengambilan selesai.")
                break

        except requests.exceptions.RequestException as e:
            print(f"Gagal mengambil data: {e}")
            return None
    
    if not all_features:
        print("Tidak ada fitur yang berhasil diunduh.")
        return None

    # --- BAGIAN PARSING MANUAL UNTUK ESRI JSON ---
    print("Mem-parsing data format Esri JSON...")
    geometries = []
    attributes = []

    for feature in all_features:
        # Ekstrak geometri (rings of coordinates)
        geom_dict = feature.get('geometry')
        if geom_dict and 'rings' in geom_dict:
            # Buat objek Poligon Shapely dari koordinat
            # Kita asumsikan ring pertama adalah batas luar
            polygon = Polygon(geom_dict['rings'][0])
            geometries.append(polygon)
            
            # Ekstrak atribut (kolom data)
            attributes.append(feature.get('attributes', {}))
    
    if not geometries:
        print("Tidak ada data geometri yang valid ditemukan.")
        return None

    # Buat GeoDataFrame dari komponen yang sudah diparsing
    gdf_all = gpd.GeoDataFrame(attributes, geometry=geometries, crs="EPSG:4326")
    return gdf_all

# --- FUNGSI UTAMA UNTUK DIJALANKAN ---
if __name__ == "__main__":
    # 1. Unduh dan parsing semua data lahan sawah
    gdf_all_sawah = parse_and_download_sawah_data()

    if gdf_all_sawah is not None and not gdf_all_sawah.empty:
        print(f"\nBerhasil mengunduh dan mem-parsing {len(gdf_all_sawah)} total poligon sawah.")
        
        # 2. Saring data secara lokal untuk mendapatkan data Yogyakarta
        provinsi_target = "DI Yogyakarta"
        print(f"Melakukan penyaringan untuk provinsi '{provinsi_target}'...")
        
        # Sesuaikan 'wadmpr' jika nama kolom provinsi di data berbeda
        # Berdasarkan JSON Anda, nama kolomnya adalah 'wadmpr'
        if 'wadmpr' in gdf_all_sawah.columns:
            gdf_sawah_diy = gdf_all_sawah[gdf_all_sawah['wadmpr'] == provinsi_target].copy()
            
            if not gdf_sawah_diy.empty:
                # 3. Simpan hasil saringan ke file
                output_filename = "Peta_Lahan_Sawah_DIY_Final.geojson"
                try:
                    gdf_sawah_diy.to_file(output_filename, driver='GeoJSON')
                    print(f"\n[SUKSES] Data lahan sawah DIY berhasil disimpan sebagai '{output_filename}'")
                    print(f"Total poligon sawah yang ditemukan untuk DIY: {len(gdf_sawah_diy)}")
                except Exception as e:
                    print(f"\n[ERROR] Gagal menyimpan file GeoJSON: {e}")
            else:
                print(f"\n[PERINGATAN] Tidak ditemukan data untuk provinsi '{provinsi_target}'.")
                print("Mungkin nama provinsi di data berbeda? (contoh: 'DI Yogyakarta')")
        else:
            print("\n[ERROR] Kolom 'wadmpr' tidak ditemukan dalam data. Tidak bisa memfilter.")

    else:
        print("\nTidak ada data yang berhasil diproses.")