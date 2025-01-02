<?php
error_reporting(E_ALL);
ini_set("display_errors", 1);

// Gelen isteğin kontrolü
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405); // Method Not Allowed
    echo json_encode(["error" => "Yalnızca POST isteklerine izin veriliyor."]);
    exit;
}

// İstek verisini al ve JSON formatında çöz
$requestBody = file_get_contents('php://input');
$data = json_decode($requestBody, true);

// Tweet içeriği kontrolü
if (!isset($data['tweet']) || empty($data['tweet'])) {
    http_response_code(400); // Bad Request
    echo json_encode(["error" => "Tweet içeriği eksik."]);
    exit;
}

function getTweetFromMessage($message, $apiKey, $maxLength = 150) {
    $url = 'https://api.openai.com/v1/chat/completions';  // Yeni endpoint (chat model için)

    // API için gerekli veri
    $data = [
        'model' => 'gpt-4', // Kullanılacak model
        'messages' => [
            ['role' => 'user', 'content' => "Lütfen şu mesaj hakkında tweet tarzında bir şey yaz: " . $message]  // Kullanıcıdan gelen mesaj
        ],
        'max_tokens' => $maxLength,  // 280 karaktere kadar tweet üretilecek
        'temperature' => 0.7, // Yanıtın yaratıcılığını ayarlayabilirsiniz
    ];

    // cURL isteği oluşturma
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/json',
        'Authorization: Bearer ' . $apiKey,
    ]);

    $response = curl_exec($ch);
    curl_close($ch);

    // Yanıtı JSON olarak al ve işleme
    if (!$response) {
        http_response_code(500);
        echo json_encode(["error" => "API isteği başarısız oldu."]);
        exit;
    }

    $responseData = json_decode($response, true);
    if (isset($responseData['choices'][0]['message']['content'])) {
        $answer = $responseData['choices'][0]['message']['content'];
    } else {
        http_response_code(500); // Internal Server Error
        echo json_encode(["error" => "API yanıtı beklenen formatta değil."]);
        exit;
    }

    // Yanıtı 200 karakterle sınırla
    $answer = substr($answer, 0, $maxLength);

    // Seo Url 
    $seoURL = strtolower($answer);
    
    // Replace spaces with dashes
    $seoURL = str_replace(' ', '-', $seoURL);
    
    // Remove non-alphanumeric characters except dashes
    $seoURL = preg_replace('/[^a-z0-9\-]/', '', $seoURL);
    
    // Optional: Replace multiple consecutive dashes with a single dash
    $seoURL = preg_replace('/-+/', '-', $seoURL);
    
    // Trim any leading or trailing dashes
    $seoURL = trim($seoURL, '-');
    
    // Kullanıcıdan gelen metni temel alarak bir web kaynağı önerisi almak
    $source = 'https://siteadi.com/link.php?q=' . $seoURL;
    
    // Yanıt ve önerilen kaynakla birlikte geri döndürme
    return [
        'answer' => $answer,
        'source' => $source
    ];
}

function shortenUrl($siteLink, $apiKey) {
    $url = "https://ay.live/api/?api=$apiKey&url=$siteLink";

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

    $response = curl_exec($ch);

    if (curl_errno($ch)) {
        echo "cURL Hatası: " . curl_error($ch);
        curl_close($ch);
        return null;
    }

    curl_close($ch);

    $responseData = json_decode($response, true);

    if ($responseData === null) {
        echo "JSON Decode Hatası: " . json_last_error_msg();
        return null;
    }

    if (isset($responseData['status']) && $responseData['status'] === 'success') {
        return $responseData['shortenedUrl'] ?? null; // Doğru alan adı
    } else {
        echo "API Hatası: ";
        print_r($responseData);
        return null;
    }
}


// Gelen tweet içeriği
$tweetContent = $data['tweet'];

$apiKey = 'chatGpt-Api-Key';
$response = getTweetFromMessage($tweetContent, $apiKey);

$Yanit =  $response['answer'];
$siteLinki =  $response['source'];
$apiKeyShort = 'ShortUrlApiKey';  // API anahtarı


// API yanıtını JSON formatında döndür
http_response_code(200); // OK
echo json_encode(["message" => $Yanit,"link" => $siteLinki]);
?>
