<?php

$accessToken = 'CQc81rb7fTzTylJ6KVqmH+PvQO3f7Hkwa6zTT5SgQ0smnnzv+Ks580Sel8FHPedCoAM82AdJxTkRn7QysM7teEbYlghyjGLukDVOfOpfNglFF+0rST//Qi24VbDVcCJ92+en5//hSvMYExMfm3JBPgdB04t89/1O/w1cDnyilFU=';

$json_string = file_get_contents('php://input');
$jsonObj = json_decode($json_string);



$type = $jsonObj->{"events"}[0]->{"message"}->{"type"};
$text = $jsonObj->{"events"}[0]->{"message"}->{"text"};
$replyToken = $jsonObj->{"events"}[0]->{"replyToken"};

if($type != "text"){
	exit;
}

$text = str_replace("'","",$text);
$text = str_replace('"','',$text);

    $fullPath =
      "python ./cgi-bin/line-gatcha.py ".$text." >./cgi-bin/line-gatcha.log";
    exec($fullPath, $outpara);

 
#$response_format_text = [
#	"type" => "text",
#	"text" => $outpara[0]
//	"text" => $fullPath
#	];


$result_image = './img/result.jpg';
$result_image2 = './img/result'.time().'.jpg';
#$result_image2 = './img/result_imgs/result'.time().'.jpg';
$command = 'cp '.$result_image.' '.$result_image2;

exec($command, $outpara);

$imagePath = 'https://koke.link/callback/'.$result_image2;


$response_format_text = [
	"type" => "image",
    "originalContentUrl" => $imagePath,
    "previewImageUrl" => $imagePath
    ];



$post_data = [
	"replyToken" => $replyToken,
	"messages" => [$response_format_text]
	];

$ch = curl_init("https://api.line.me/v2/bot/message/reply");
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'POST');
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($post_data));
curl_setopt($ch, CURLOPT_HTTPHEADER, array(
    'Content-Type: application/json; charser=UTF-8',
    'Authorization: Bearer ' . $accessToken
    ));
$result = curl_exec($ch);
curl_close($ch);

?>

