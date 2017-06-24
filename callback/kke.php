<?php

$accessToken = 'yujKheKG1DXIoS/vuRsj83AcstuBUQWpsFeZQ5IQuU21ed6NUdI4TdoSS4lfWXVIyMOsMTlrS9bt4NaAwxIwRXPELFItvfy0UrlNfkW/17DEe6mOCCPEc5U2RM0x9CtI6i3sNMqFuV/66p8ZyMDTYAdB04t89/1O/w1cDnyilFU=';

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
  "python ./cgi-bin/translate.py '".$text."'";

exec($fullPath, $outpara);

 
$response_format_text = [
	"type" => "text",
	"text" => $outpara[0]
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

