import pandas as pd
import numpy as np

try:
    df_original = pd.read_csv('../../dataset/dataset_yogyakarta_realistis.csv')

    tanaman_yogyakarta_final = [
        # Pertanian
        'rice',
        'maize',
        'soybean',
        'mungbean',
        'peanut',
        'sweetpotato',
        'cassava',
        # Hortikultura
        'mango',
        'orange',
        'papaya',
        'banana',
        'shallots',
        'garlic',
        'chilli',
        'chives',
        'cabbage',
        'watermelon',
        'muskmelon',
        # Perkebunan
        'tea',
        'coffee',
    ]
    
    df_base = df_original[df_original['label'].isin(tanaman_yogyakarta_final)].copy()
    print(f"Dataset dasar dengan {len(df_base['label'].unique())} tanaman berhasil disiapkan, berisi {len(df_base)} baris data.")
    
    print("Memulai proses augmentasi data untuk memperbanyak jumlah sampel...")
    
    augmentation_factor = 2
    augmented_data = []

    for _, row in df_base.iterrows():
        
        augmented_data.append(row.to_dict())
        
        for _ in range(augmentation_factor):
            new_row = row.to_dict()
            
            new_row['nitrogen'] += np.random.randint(-3, 4)
            new_row['phosphorous'] += np.random.randint(-2, 3)
            new_row['potassium'] += np.random.randint(-2, 3)
            new_row['temperature'] += np.random.uniform(-0.5, 0.5)
            new_row['humidity'] += np.random.uniform(-1.0, 1.0)
            new_row['ph'] += np.random.uniform(-0.1, 0.1)
            new_row['rainfall'] += np.random.uniform(-2.0, 2.0)
            
            for key in ['nitrogen', 'phosphorous', 'potassium', 'ph', 'rainfall']:
                if new_row[key] < 0:
                    new_row[key] = 0

            augmented_data.append(new_row)

    
    df_augmented = pd.DataFrame(augmented_data)
    df_augmented = df_augmented.sample(frac=1).reset_index(drop=True)

    
    nama_file_baru = '../../dataset/dataset_yogyakarta_augmented.csv'
    df_augmented.to_csv(nama_file_baru, index=False)
    
    
    print("\nProses augmentasi data selesai.")
    print(f"Dataset baru yang telah diperbanyak telah disimpan sebagai: '{nama_file_baru}'")
    
    print("\n--- Perbandingan Jumlah Data ---")
    print(f"Jumlah baris data sebelum augmentasi: {len(df_base)}")
    print(f"Jumlah baris data setelah augmentasi: {len(df_augmented)}")
    print(f"Total data berhasil ditingkatkan menjadi {len(df_augmented) / len(df_base):.0f}x lipat.")


except FileNotFoundError:
    print("File 'dataset' tidak ditemukan. Pastikan file sudah diunggah dengan benar.")
except Exception as e:
    print(f"Terjadi kesalahan: {e}")