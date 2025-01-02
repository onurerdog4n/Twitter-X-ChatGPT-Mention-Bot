<?php
// Veritabanı bağlantısı ayarları
$host = 'localhost'; // Veritabanı sunucusu
$dbname = 'linkServices'; // Veritabanı adı
$username = 'linkServices'; // Veritabanı kullanıcı adı
$password = '6wVr3*7i1'; // Veritabanı şifresi

try {
    // PDO ile veritabanı bağlantısını kur
    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die("Veritabanı bağlantısı başarısız: " . $e->getMessage());
}

// IP adresini al
$ip = $_SERVER['REMOTE_ADDR'];

// İstanbul saatine göre tarih ve saat
date_default_timezone_set('Europe/Istanbul');
$dateTime = date('Y-m-d H:i:s');

// URL parametresinden q değerini al
$q = isset($_GET['q']) ? $_GET['q'] : '';

// visitors tablosuna verileri ekle
try {
    $stmt = $pdo->prepare("INSERT INTO visitors (ip, date_time, location, query) VALUES (:ip, :date_time, :location, :query)");
    $stmt->execute([
        ':ip' => $ip,
        ':date_time' => $dateTime,
        ':location' => 'ISTANBUL',
        ':query' => $q
    ]);
} catch (PDOException $e) {
    die("Veri ekleme hatası: " . $e->getMessage());
}

// 404 Not Found mesajını yazdır
http_response_code(404);
echo "<h1>404 Not Found</h1>";
echo "<p>Aradığınız sayfa bulunamadı.</p>";

?>
