import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

def plot_distribusi_kelas(dataframe, kolom_label):
    """Menampilkan grafik batang untuk melihat jumlah data per tanaman."""
    plt.figure(figsize=(12, 8))
    sns.countplot(y=dataframe[kolom_label], order=dataframe[kolom_label].value_counts().index, palette='viridis')
    plt.title(f'Distribusi Jumlah Data per Tanaman', fontsize=16)
    plt.xlabel('Jumlah Sampel Data', fontsize=12)
    plt.ylabel('Nama Tanaman', fontsize=12)
    plt.tight_layout()
    plt.show()

def plot_korelasi_fitur(dataframe, fitur_list):
    """Menampilkan heatmap korelasi untuk melihat hubungan antar fitur."""
    plt.figure(figsize=(10, 7))
    correlation_matrix = dataframe[fitur_list].corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Heatmap Korelasi Antar Fitur', fontsize=16)
    plt.show()

if __name__ == "__main__":
    df_master = pd.read_csv('../../dataset/dataset_yogyakarta_augmented.csv')

    plot_distribusi_kelas(df_master, 'label')

    fitur = ['temperature', 'humidity', 'rainfall']
    plot_korelasi_fitur(df_master, fitur)