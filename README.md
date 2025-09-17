Web: https://tsaniya-fini-footballshop.pbp.cs.ui.ac.id/

<details>
<summary>Tugas individu 2: Implementasi Model-View-Template (MVT) pada Django</summary>

**Menyiapkan Virtual Environment dan dependencies**
Pertama-tama saya membuat dan masuk ke direktori proyek `football-shop` melalui terminal. Di dalam direktori tersebut, saya membuat virtual enviroment dan langsung mengaktifkannya. Setelah virtual enviroment aktif, saya buat berkas `requirements.txt` yang berisi daftar semua dependencies yang diperlukan seperti django, dll. Terakhir saya menginstall semua dependencies tersebut.

**Membuat sebuah proyek django baru**

1.  Menjalankan perintah berikut untuk membuat proyek.

    ```bash
    django-admin startproject football_shop .
    ```

    Perintah ini akan menghasilkan struktur direktori dan berkas-berkas dasar yang dibutuhkan untuk proyek django

2.  Membuat file `.env` di dalam direktori root proyek

3.  Membuka file `.env` dan menambahkan konfigurasi berikut:
    ```python
    PRODUCTION=False
    ```

4.  Membuat juga file `.env.prod` di direktori yang sama untuk konfigurasi production:

    ```python
    DB_NAME=<nama database>
    DB_HOST=<host database>
    DB_PORT=<port database>
    DB_USER=<username database>
    DB_PASSWORD=<password database>
    SCHEMA=tugas_individu
    PRODUCTION=True
    ```

5.  Memodifikasi file `settings.py` untuk menggunakan environment variables. Menambahkan kode berikut di bagian atas file (setelah import Path):

    ```python
    import os
    from dotenv import load_dotenv
    # Load environment variables from .env file
    load_dotenv()
    ```
6.  Menambahkan kedua string berikut pada ALLOWED_HOSTS di settings.py untuk keperluan development:

    ```python
    ...
    ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
    ...
    ```

7.  Menambahkan konfigurasi `PRODUCTION` tepat di atas code `DEBUG` di `settings.py.`

    ```python
    PRODUCTION = os.getenv('PRODUCTION', 'False').lower() == 'true'
    ```

8. Mengonfigurasi pengaturan basis data. Dengan menggunakan variabel `PRODUCTION` yang sudah dibuat, `settings.py` diatur menggunakan conditional. Jika `PRODUCTION` bernilai True, django akan terhubung ke basis data PostgreSQL menggunakan kredensial yang diambil dari variabel lingkungan di berkas .env.prod. Sebaliknya, jika PRODUCTION bernilai False, django akan menggunakan basis data SQLite yang lebih sederhana untuk keperluan pengembangan lokal. Ini memastikan bahwa konfigurasi sensitif untuk production tidak tercampur dengan pengaturan untuk pengembangan.

**Membuat aplikasi dengan nama `main` pada proyek tersebut.**
1.  Menjalankan perintah ini:

    ```bash
    python manage.py startapp main
    ```

3.  Selanjutnya, mendaftarkan aplikasi `main` ini ke dalam proyek. Membuka file `football_shop/settings.py`, ke bagian `INSTALLED_APPS`, dan menambahkan main di dalamnya.

    ```python
    # football_shop/settings.py

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'main', # menambahkan ini
    ]
    ```

    INSTALLED_APPS yang ada pada berkas settings.py berguna agar proyek django bisa mengenali dan mengelola aplikasi main ke dalam proyek footbal shop.

**Membuat dan Mengisi Berkas `main.html`**
1.  Di dalam folder `main`, membuat direktori baru bernama `templates`.

2.  Di dalam folder `templates`, membuat berkas baru bernama `main.html`. Berkas ini yang akan menjadi kerangka dari page atau halaman

3.  Mengisi berkas `main.html` dengan kode berikut. Kode di dalam `{{ }}` adalah variabel yang dikirim dari `views.py`.

    ```html
    <h1>Football Shop</h1>

    <h4>App Name: </h4>
    <p>{{app_name}}</p> 
    <h4>Name: </h4>
    <p>{{nama}}</p> 
    <h4>Class: </h4>
    <p>{{class}}</p> 
    ```

**Membuat model pada aplikasi `main` dengan nama `Product` dan memiliki atribut wajib sebagai berikut.**
1.  Membuka file berkas `models.py` pada direktori aplikasi `main`.

2.  Menulis kode berikut untuk membuat class `Product` dengan atribut-atribut yang sudah ditentukan

    ```python
    # main/models.py
    from django.db import models

    class Product(models.Model):
        name = models.CharField(max_length=255)
        price = models.IntegerField()
        description = models.TextField()
        thumbnail = models.URLField()
        category = models.CharField(max_length=100)
        is_featured = models.BooleanField(default=False)
    ```

3.  Setelah model didefinisikan, saya menjalankan python manage.py makemigrations di terminal untuk membuat berkas migrasi, yaitu rencana perubahan database agar sesuai dengan model (belum diaplikasikan ke dalam basis data.). Lalu jalankan python manage.py migrate untuk mengeksekusi berkas migrasi tersebut sehingga perubahan benar-benar diterapkan ke basis data.

**Membuat sebuah fungsi pada views.py untuk dikembalikan ke dalam sebuah template HTML yang menampilkan nama aplikasi serta nama dan kelas.**
1.  Membuka berkas `views.py` yang terletak di dalam berkas aplikasi `main`

2.  Menulis kode berikut. Fungsi ini akan menyiapkan data (nama aplikasi, nama, dan kelas) dan mengirimkannya ke berkas HTML.

    ```python
    # main/views.py
    from django.shortcuts import render

    def show_main(request):
        context = {
            'app_name': 'My Football Shop', 
            'name': 'Tsaniya',   
            'class': 'PBP E'   
        }

        return render(request, "main.html", context)
    ```

    Fungsi view adalah menerima request, memprosesnya (misalnya mengambil data dari basis data atau menyiapkan data), dan kemudian mengembalikan sebuah response. Dalam kasus ini, fungsi `show_main` menyiapkan sebuah `dictionary` bernama `context` yang berisi data yang ingin ditampilkan (nama aplikasi, nama, dan kelas). Kemudian, fungsi `render` dipanggil untuk menggabungkan data dari `context` ini dengan sebuah template html (`main.html`) untuk menghasilkan halaman web yang sesuai.

**Membuat sebuah routing pada urls.py aplikasi main untuk memetakan fungsi yang telah dibuat pada views.py**

Untuk menghubungkan fungsi view dengan URL yang bisa diakses oleh pengguna, proses routing dibagi menjadi dua tahap. Pertama, buat berkas baru `urls.py` di dalam direktori aplikasi `main`. Berkas ini berfungsi untuk mendaftarkan semua URL yang spesifik untuk aplikasi `main`, di mana setiap path URL (misalnya, path kosong '') dipetakan ke fungsi view yang sesuai (seperti `show_main`). Kedua, agar URL aplikasi ini dikenali oleh proyek utama, berkas `urls.py` di tingkat proyek harus dimodifikasi. Dengan menggunakan fungsi include, path URL utama (path kosong '') diatur untuk mendelegasikan atau menyertakan semua pola URL yang telah didefinisikan di dalam berkas `main/urls.py.`

**Melakukan deployment ke PWS terhadap aplikasi yang sudah dibuat sehingga nantinya dapat diakses oleh teman-teman melalui Internet**
1.  Sebelum deployment, saya mengunggah proyek ke repositori github terlebih dahulu. Setelah itu, di PWS saya membuat proyek baru dengan nama footbalshop. Dari pembuatan proyek ini, saya mendapatkan Project Command dan Project Credentials yang penting untuk langkah selanjutnya dan harus disimpan terlebih dahulu. Langkah selanjutnya menyalin isi berkas `.env.prod` ke dalam Raw Editor di tab Environs proyek, serta memastikan variabel SCHEMA dan PRODUCTION sudah diatur dengan benar.

2.  Selanjutnya, di dalam berkas `settings.py` pada tingkat proyek harus diperbarui dengan menambahkan URL deployment PWS ke daftar `ALLOWED_HOST`
    ```bash
    ALLOWED_HOSTS = ["localhost", "127.0.0.1", "tsaniya-fini-footballshop.pbp.cs.ui.ac.id"]
    ```

    Perubahan ini kemudian disimpan dan diunggah lagi ke repositori github. Selanjutnya, menjalankan perintah yang terdapat pada informasi Project Command pada halaman PWS. Ketika melakukan push ke PWS, akan ada window yang meminta username dan password dari Project Credentials yang telah disimpan sebelumnya.

3.  Setelah proses push ke PWS selesai, status deployment dapat diverifikasi melalui page yang ada di PWS. Jika status proyek menunjukkan Running, artinya aplikasi telah berhasil di-deploy dan sudah dapat diakses melalui URL yang disediakan. Tombol `View Project` pada halaman tersebut bisa digunakan untuk langsung mengunjungi aplikasi yang sudah aktif.

-----

**Buatlah bagan yang berisi request client ke web aplikasi berbasis Django beserta responnya dan jelaskan pada bagan tersebut kaitan antara urls.py, views.py, models.py, dan berkas html.**

LINK: https://drive.google.com/file/d/1Vu4F-vF-Afi4ywNeeOV0ZoSXeKoUgRIV/view?usp=sharing

Client mengirimkan request ke sebuah URL. Django menerima request dan mencocokkan URL tersebut dengan urls.py di proyek. urls.py proyek mengarahkan request ke urls.py di aplikasi main. Jika urls.py main menemukan path yang cocok akan memanggil fungsi yang sesuai di views.py. Jika memerlukan data, views akan berinteraksi dengan models.py untuk mengambil data dari basis data. Setelah mendapatkan data, views.py akan memanggil berkas template html dan mengirim data ke dalam template. Template html yang sudah berisi data tersebut kemudian diubah menjadi response HTTP dan dikirim kembali ke Client untuk ditampilkan.

**Jelaskan peran `settings.py`\!** 

`settings.py` adalah berkas yang berfungsi sebagai pusat kendali dan konfigurasi utama untuk sebuah proyek django. Di dalam berkas ini, semua aplikasi yang aktif di dalam proyek didaftarkan, dan semua pengaturan penting didefinisikan. Hal ini mencakup konfigurasi koneksi ke basis data, pengaturan keamanan fundamental seperti SECRET_KEY, ALLOWED_HOST, dan DEBUG. Selain itu, settings.py juga bertanggung jawab untuk menentukan lokasi file statis (seperti HTML, CSS, dll.), mengatur alur pemrosesan request dan response melalui middleware, serta mengelola pengaturan lokalisasi seperti bahasa dan zona waktu. 

**Bagaimana cara kerja migrasi database di Django?**

Migrasi adalah cara Django untuk menyinkronkan perubahan pada `models.py` dengan skema database.
1.  `python manage.py makemigrations`: django akan membandingkan `models.py` saat ini dengan berkas migrasi terakhir. Lalu jika ada perubahan (misalnya menambah field baru), django akan membuat berkas migrasi baru di direktori migrations. Berkas ini berisi instruksi dalam bahasa python tentang cara menerapkan perubahan tersebut ke basis data.
2.  `python manage.py migrate`: django akan mengeksekusi semua berkas migrasi yang belum dieksekusi. Perintah ini membaca instruksi dari berkas migrasi dan menerjemahkannya menjadi perintah SQL (seperti untuk membuat tabel, mengubah struktur kolom, atau menghapus sesuatu) yang sesuai untuk dijalankan pada basis data.

**Mengapa framework Django dijadikan permulaan pembelajaran?** 

Framework java dijadikan permulaan pembelajaran karena memiliki banyak kelebihan seperti:
* Django memiliki dokumentasi resmi yang jelas dan banyak secara open-source. Komunitasnya yang besar juga berarti hampir setiap masalah yang mungkin dihadapi pemula sudah pernah ditanyakan dan dijawab di forum seperti Stack Overflow.
* Django memiliki sistem autentikasi pengguna, dan sudah termasuk dengan Clickjacking, Cross-Site Scripting (XSS), Cross-Site Request Forgery (CSRF), dan SQL injection protection. Fitur-fitur ini sudah tersedia, jadi kita tidak perlu untuk memasangnya secara manual.
* django mengadopsi pendekatan python "batteries included”, Django memiliki banyak fitur yang sudah siap pakai. Jadi programmer tidak perlu membuat programnya dari nol

**Apakah ada feedback untuk asisten dosen tutorial 1 yang telah kamu kerjakan sebelumnya?** 

Sampai saat ini belum ada feedback yang mau saya sampaikan
</details>

<details>
<summary>Tugas individu 3: Implementasi Form dan Data Delivery pada Django</summary>

**Jelaskan mengapa kita memerlukan data delivery dalam pengimplementasian sebuah platform?**
Kita memerlukan data delivery untuk memungkinkan aplikasi atau platform yang berbeda saling berkomunikasi dan berbagi data. Contoh implementasi: Saat kita mencari jersey di aplikasi, aplikasi mengirim request ke server. Server membalas dengan daftar produk yang relevan dalam format json. Aplikasi kemudian mengubah data json ini menjadi tampilan daftar produk yang kita lihat di layar. Jadi, data delivery penting untuk komunikasi, sinkronisasi, dan pertukaran informasi antara bagian-bagian sistem atau platform.

**Menurutmu, mana yang lebih baik antara XML dan JSON? Mengapa JSON lebih populer dibandingkan XML?**
Menurut saya yang jauh lebih baik adalah JSON karena sintaks JSON lebih padat, mudah dibaca, dan mudah ditulis. Sebaliknya, sintaks XML lebih panjang dan rinci. JSON menghasilkan ukuran file yang lebih kecil, sehingga transmisi datanya lebih cepat. XML, memiliki struktur yang lebih kompleks sehingga menghasilkan ukuran file yang memakan lebih banyak ruang. JSON lebih sederhana dan fleksibel dalam hal skema dokumentasi. JSON lebih aman daripada XML, karena XML memerlukan konfigurasi tambahan untuk mitigasi risiko keamanan.

**Jelaskan fungsi dari method is_valid() pada form Django dan mengapa kita membutuhkan method tersebut?**
is_valid() digunakan untuk memastikan semua data yang diisi sudah sesuai, contoh field harga harus angka. Is_valid() sangat dibutuhkan agar agar data yang masuk ke sistem terjamin aman dan sesuai format sebelum diproses (misalnya disimpan ke database).

**Mengapa kita membutuhkan csrf_token saat membuat form di Django? Apa yang dapat terjadi jika kita tidak menambahkan csrf_token pada form Django? Bagaimana hal tersebut dapat dimanfaatkan oleh penyerang?**
CSRF token dibutuhkan untuk mencegah serangan CSRF. Serangan CSRF sendiri adalah pengguna dibuat seolah-olah meminta request tertentu pada website dan kemudian web akan mengeksekusi permintaan tersebut. CSRF token merupakan token unik untuk memastikan request benar-benar berasal dari pengguna yang benar, bukan dari pengguna lain.

**Mengakses keempat URL di poin 2 menggunakan Postman, membuat screenshot dari hasil akses URL pada Postman, dan menambahkannya ke dalam README.md.**
https://drive.google.com/file/d/1hdtlWKq6skRXmHaZuIi3wFNU1UFCW8es/view?usp=sharing

-----
**Tambahkan 4 fungsi views baru untuk melihat objek yang sudah ditambahkan dalam format XML, JSON, XML by ID, dan JSON by ID.**

Pertama saya membuka `views.py` yang ada pada direktori main dan menambahkan import `HttpResponse` dan `Serializer` pada bagian atas. Lalu membuat fungsi baru dengan nama `show_xml` dan `show_json` yang keduanya berfungsi untuk mengambil seluruh data dari model `Product` menggunakan `Product.objects.all()`. Data query yang didapat kemudian diubah formatnya dengan fungsi `serializers.serialize()`, dengan format xml dan json. Hasil dari serialisasi kemudian di return sebagai sebuah `HttpResponse`, dengan content_type diatur ke application/xml atau application/json agar browser lain dapat menginterpretasikan data dengan benar.

Selain itu, saya juga membuat fungsi berdasarkan id, yaitu `show_xml_by_id` dan `show_json_by_id`, yang menerima parameter id dari url. Di dalam kedua fungsi ini, data diambil dengan `Product.objects.filter(pk=id)`. Untuk mengantisipasi kondisi ketika data dengan product_id tertentu tidak ditemukan dalam basis data, saya menambahkan `try...except`. Jika terjadi Product.DoesNotExist, maka fungsi akan mengembalikan HttpResponse dengan status 404 sebagai tanda data tidak ada.

**Membuat routing URL untuk masing-masing `views` yang telah ditambahkan pada poin 1.**

Membuka `urls.py` yang ada pada direktori `main` dan import fungsi yang sudah dibuat sebelumnya, seperti  `show_xml`, `show_json`, serta `show_xml_by_id` dan `show_json_by_id`. Setelah diimpor, saya menambahkan path baru ke dalam urlpatterns.
```python
...
path('xml/', show_xml, name='show_xml'),
path('json/', show_json, name='show_json'),
path('xml/<str:news_id>/', show_xml_by_id, name='show_xml_by_id'),
path('json/<str:news_id>/', show_json_by_id, name='show_json_by_id')
...
```
bagian <str:product_id> berfungsi untuk menangkap id dari URL dan meneruskannya sebagai parameter ke dalam fungsi view

**Membuat halaman yang menampilkan data objek model yang memiliki tombol "Add" yang akan redirect ke halaman `form`, serta tombol "Detail" pada setiap data objek model yang akan menampilkan halaman detail objek.**

Pada tahap ini, saya memodifikasi template `main.html` agar extends base.html dan menambahkan sebuah tombol yang mengarah ke halaman add product `{% url 'main:add_product' %}`. Di dalam template ini, saya membuat loop `{% for product in product_list %}` untuk menampilkan setiap item dari product_list. Masing-masing produk ditampilkan beserta informasi utamanya seperti nama, kategori, thumbnail, dan deskripsi singkat. Selain itu, saya menambahkan tombol "Detail" yang tautannya dibuat untuk setiap produk menggunakan product.id, yang akan mengarahkan pengguna ke halaman detail spesifik produk tersebut. Terdapat juga kondisi jika product_list kosong, di mana sebuah pesan akan ditampilkan untuk memberitahu bahwa belum ada produk yang tersedia

**Membuat halaman form untuk menambahkan objek model pada app sebelumnya.**

Untuk membuat halaman form, pertama membuat berkas `main.form.py`. Di dalamnya saya membuat class `ProductForm` yang mewarisi `ModelForm`, yang secara otomatis menghasilkan field-field form berdasarkan model `Product` yang telah ditentukan. Selanjutnya pada views.py saya membuat fungsi `add_product` yang bertujuan untuk menampilkan halaman dengan form kosong saat menerima request GET, dan akan memvalidasi serta menyimpan data yang dikirim saat menerima request POST menggunakan `form.is_valid()` dan `form.save()`, sebelum akhirnya kembali ke halaman utama. Tampilan dari form saya buat dalam template `add_product.html`, yang berisi tag <form> dengan method "POST" menyertakan {% csrf_token %} untuk keamanan, dan merender field form dengan {{ form.as_table }}. Terakhir, agar halaman form ini dapat diakses, saya menambahkan path('add-product/', ...) pada urls.py yang menghubungkan URL tersebut ke fungsi add_product.

**Membuat halaman yang menampilkan detail dari setiap data objek model.**

Untuk membuat halaman detail setiap produk, pertama saya membuat fungsi view baru bernama detail_product di views.py yang menerima parameter id. Fungsi ini menggunakan get_object_or_404 untuk mengambil satu objek Product berdasarkan id-nya, di mana jika objek tidak ditemukan akan otomatis menampilkan halaman 404. Objek yang berhasil diambil kemudian dikirimkan ke sebuah template baru, detail_product.html, yang dibuat untuk menampilkan semua atribut detail dari produk tersebut seperti nama produk dan deskripsi. Agar halaman ini dapat diakses, saya menambahkan sebuah path baru di urls.py dengan pola 'product/<str:id>/', yang berfungsi menangkap id dari URL dan menghubungkannya ke fungsi detail_product.
</details>
