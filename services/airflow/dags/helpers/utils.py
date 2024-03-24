from datetime import datetime

def hitung_umur(tanggal_lahir):
    # Mengkonversi tanggal lahir menjadi objek datetime
    tanggal_lahir = datetime.strptime(tanggal_lahir, "%Y-%m-%d")
    
    # Mendapatkan tanggal saat ini
    tanggal_sekarang = datetime.now()
    
    # Menghitung selisih tahun antara tanggal lahir dan tanggal sekarang
    umur = tanggal_sekarang.year - tanggal_lahir.year
    
    # Menyesuaikan umur jika belum berulang tahun pada tahun ini
    if tanggal_lahir.month > tanggal_sekarang.month or (tanggal_lahir.month == tanggal_sekarang.month and tanggal_lahir.day > tanggal_sekarang.day):
        umur -= 1
    
    return umur

def extract_date_tanggal_umur(date_string):
    # Membuat dictionary untuk mapping nama bulan ke angka bulan
    bulan_dict = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'Mei': '05', 'Jun': '06',
                  'Jul': '07', 'Agt': '08', 'Sep': '09', 'Okt': '10', 'Nov': '11', 'Des': '12'}

    # Memisahkan string tanggal menjadi komponen-komponennya
    tanggal_parts = date_string.split()

    # Mendapatkan tanggal, bulan, dan tahun dari string
    tanggal_str = tanggal_parts[0]
    bulan_str = bulan_dict[tanggal_parts[1]]
    tahun_str = tanggal_parts[2]

    # Menggabungkan komponen tanggal menjadi string dalam format YYYY-mm-dd
    tanggal_format = f"{tahun_str}-{bulan_str}-{tanggal_str}"

    # Mengonversi string tanggal_format menjadi objek datetime
    tanggal_obj = datetime.strptime(tanggal_format, '%Y-%m-%d')

    # Mengambil hanya tanggal dari objek datetime
    tanggal_tanpa_time = tanggal_obj.date()

    return tanggal_tanpa_time

def extract_date(date_string):
    # Membuat dictionary untuk mapping nama bulan ke dalam format yang sesuai
    bulan_dict = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'Mei': '05', 'Jun': '06',
                  'Jul': '07', 'Agt': '08', 'Sep': '09', 'Okt': '10', 'Nov': '11', 'Des': '12'}

    # Memisahkan string tanggal menjadi komponen-komponennya
    tanggal_parts = date_string.split()

    # Mengganti nama bulan dengan format yang sesuai
    bulan_str = bulan_dict.get(tanggal_parts[1], tanggal_parts[1])

    # Menggabungkan kembali string tanggal yang telah dimodifikasi
    tanggal_string_modif = f"{tanggal_parts[0]} {bulan_str} {tanggal_parts[2]}"

    # Membuat objek datetime dari string yang telah dimodifikasi
    tanggal_obj = datetime.strptime(tanggal_string_modif, '%d %m %Y')

    # Mengambil hanya tanggal dari objek datetime
    tanggal_tanpa_time = tanggal_obj.date()

    return tanggal_tanpa_time

def convert_to_billion(amount_string):
    # Hilangkan karakter 'Rp' dan 'Mlyr.'
    amount_string = amount_string.replace('Rp', '').replace('Mlyr.', '')
    # Hilangkan tanda titik sebagai pemisah ribuan
    amount_string = amount_string.replace('.', '')
    # Ganti koma dengan titik untuk memisahkan bagian pecahan
    amount_string = amount_string.replace(',', '.')
    # Konversi string menjadi float
    amount_in_billion = float(amount_string) * 1000000000
    return int(amount_in_billion)