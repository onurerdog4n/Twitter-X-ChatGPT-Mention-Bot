Bu proje, tweet içeriklerini işleyerek ChatGPT API aracılığıyla bir mention oluşturur, ardından siteadi.com üzerinden bir spam linki oluşturur ve bu linki bir link kısaltma servisi aracılığıyla kısaltır. Bu süreç, ziyaretçileri veritabanına kaydetmek için tasarlanmıştır.



README.md
Spam Link Oluşturucu ve Mention Botu
Bu proje, tweet içeriklerini işleyerek ChatGPT API aracılığıyla bir mention oluşturur, ardından siteadi.com üzerinden bir spam linki oluşturur ve bu linki bir link kısaltma servisi aracılığıyla kısaltır. Bu süreç, ziyaretçileri veritabanına kaydetmek için tasarlanmıştır.

Çalışma Şekli
Tweet İşleme:

Tweet içeriği, ChatGPT API’ye gönderilir ve tweet hakkında bir mention oluşturulur.
Spam Link Oluşturma:

Mention, siteadi.com üzerinde bir spam linkle birleştirilir.
Link Kısaltma:

Spam link, TR.link API'si aracılığıyla kısaltılır.
Örnek Mention Formatı: "Dominik Livakovic, kaleci performansını yeni seviyelere taşıyor. Oyun okuma yeteneği ve refleksleri, onu durdurulamaz yapıyor. #Livakovic #Futb || DETAY : https://ay.live/TbZ"

Gereksinimler
Projenin çalışması için aşağıdaki yazılım ve API anahtarlarına ihtiyaç vardır:

Kurulması Gereken Paketler
selenium==4.27.1
webdriver-manager==4.0.2
Pillow==10.0.0
python-dotenv==1.0.1

API Anahtarları
ChatGPT API Key: OpenAI API’ye erişim için gerekli.
TR.link API Key: Link kısaltma servisi için gerekli.

Kurulum

main.py Düzenlemeleri

AccountMail = "E-posta adresinizi girin"
AccountUsername = "Kullanıcı adınızı girin"
AccountPassword = "Şifrenizi girin"
siteadi.com geçen alanları kendi web sitenizle değiştirin.
get_shortened_url fonksiyonunda, TR.link API anahtarınızı ekleyin

api.php Düzenlemeleri
$apiKey = "ChatGPT-Api-Key'inizi ekleyin";

link.php Düzenlemeleri
$dbHost = "Veritabanı sunucusunu girin";
$dbUser = "Veritabanı kullanıcı adınızı girin";
$dbPass = "Veritabanı şifrenizi girin";
$dbName = "Veritabanı adınızı girin";


