<?php

$accessToken = 'daAevLmHJIeqvXBQ+oet1G/CRJROVvr78byQ5DOeJsmhZv28BFK8wo3D247qPq027I8jyx7LXkuyVnZOpHLubmQwmk4mBFknY9JLIZg7y3aZeZDL1saM1NLl7Myz8O+gBHhtFA3h7JyOgoKEX55XOQdB04t89/1O/w1cDnyilFU=';


$json_string = file_get_contents('php://input');
$jsonObj = json_decode($json_string);



$type = $jsonObj->{"events"}[0]->{"message"}->{"type"};
$text = $jsonObj->{"events"}[0]->{"message"}->{"text"};
$replyToken = $jsonObj->{"events"}[0]->{"replyToken"};

if($type != "text"){
	exit;
}

$response_format_text = [
	"type" => "text",
	"text" => "yeeeee"
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

