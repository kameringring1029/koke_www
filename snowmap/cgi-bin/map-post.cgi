#! /usr/bin/perl 
=pod
use warnings;
use strict;
=cut

#use strict;
use CGI;
use CGI::Carp qw(fatalsToBrowser);


use XML::Simple;
use Data::Dumper;
{
    no warnings 'redefine';
    package Data::Dumper;
    sub qquote { return shift; }
}
$Data::Dumper::Useperl = 1;

require 'jcode.pl';
read( STDIN, $data, $ENV{ 'CONTENT_LENGTH' } );


my $ln = "\x0A";

my $maxd = 0;
my $predist = "";
my $predist00 = 0;
my $predist0 = 0;
my $predist1 = 0;
my $decflag = 0;
my $firstdist = 0;

my $thermo = 0;
# 4℃以上なら降雪と認めない
my $thermothre = 4;

# アルゴリズムの頻度閾値
my $threnum = 100;
my $term = 600;

#my $outputfn = "/var/www/snowmap/perl/sens.csv";
my $outscfn = "/var/www/snowmap/log/snowcover/cover";
my $prefn = "/var/www/snowmap/log/presc/presc";
#my $outraw = "/var/www/snowmap/log/2013/scraw.csv";
my $outrawfn = "/var/www/snowmap/log/rawdata/rawdata";
my $outfall = "/var/www/snowmap/perl/fall.csv";
my $outscat = "/var/www/snowmap/perl/scat.csv";
my $XML = "/var/www/snowmap/log/sens.xml";

my @spline;
my @sc; my @times;
my $avesc = 0;
my $fall = 0;
my $scat = 0;
my $wtime;
my $writeline;
my $locnum;


# POSTデータの受け取り
$data =~ tr/+/ /;
$data =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack('C', hex($1) )/ge;
&jcode'convert( *value, 'sjis' );
chomp $data;

#($head,$data)=split(/=/,$data);
#my @lines=split(/,e$ln/,$data);


print "Content-type: text/html\n\n";

print "---curl---$ln";

#print "$data$ln";

($locno, $data) = split(/#/,$data);

print "locno = $locno$ln";
#$outraw = $outraw.".$locno";
$outrawfn = $outrawfn."$locno".".csv";
#$outputfn = $outputfn.".$locno";
$outscfn = $outscfn."$locno".".csv";
$prefn = $prefn.".$locno";
$outfall = $outfall.".$locno";
$outscat = $outscat.".$locno";


#センサから地面までの初期値
if($locno == 1){ $maxd = 500;
}elsif($locno == 2){ $maxd = 550;
}elsif($locno == 3){ $maxd = 550;
}elsif($locno == 4){ $maxd = 550;
}elsif($locno == 5){ $maxd = 530;
}elsif($locno == 6){ $maxd = 500;
#}elsif($locno == 7){ $maxd = 500;
#}elsif($locno == 8){ $maxd = 500;
}


&setpre();


#open(W, ">> $outraw") or die;
open(RAW, ">> $outrawfn") or die;
#flock(W, 2);
flock(RAW, 2);

@splines = split(/e/,$data);
for(my $l=0; $l<=$#splines; $l++){
#	print "splines[$l] = $splines[$l]$ln";
	my $sensor;
	($sensor, $times[$l]) = split(/,/,$splines[$l]);
#	if($l==0 && $locno==6){ $times[$l] = $times[$l]+11540405;}
	if($l!=0){ $times[$l] = $times[0]+$l/10;}
	(my $rhin, $sc[$l]) = split(/R/,$sensor);
	$sc[$l] = $sc[$l] + 0;
#	print "$times[$l], $sc[$l]<br>$ln";
#	print "sc = $sc[$l]$ln";
#	print W "$times[$l],$sc[$l]$ln";
	print RAW "$times[$l],$sc[$l]$ln";
	$sc[$l] = $maxd - $sc[$l];
}

#print "sclength = $#times<br>$ln";

#close W;
close RAW;

&calc();


sub calc{

	my @termsc; my @termtime;
	my $decrease = 0;

	for(my $i=0; $i<$#sc/$term; $i++){

		my @sclognum = ("0")x11;	# 要素0を10列
		my @sclog = ("0")x11;

		my $naflag = 0;

		print "$i : $times[$i*$term] : $sc[$i*$term] :";
		
		# センサデータ分類
		for(my $j=0; $j<$term; $j++){
			if($sc[$i*$term + $j] > $predist + 5.0){
				$sclognum[1]++;
				$sclog[1] = $sc[$i*$term + $j];
			}elsif(($sc[$i*$term + $j] <= $predist + 5.0) && ($sc[$i*$term + $j] > $predist + 2.0)){
				$sclognum[2]++;
				$sclog[2] = $sc[$i*$term + $j];
			}elsif(($sc[$i*$term + $j] <= $predist + 2.0) && ($sc[$i*$term + $j] > $predist + 1.5)){
				$sclognum[3]++;
				$sclog[3] = $sc[$i*$term + $j];
			}elsif(($sc[$i*$term + $j] <= $predist + 1.5) && ($sc[$i*$term + $j] > $predist + 1.0)){
				$sclognum[4]++;
				$sclog[4] = $sc[$i*$term + $j];
			}elsif(($sc[$i*$term + $j] <= $predist + 1.0) && ($sc[$i*$term + $j] > $predist + 0.5)){
				$sclognum[5]++;
				$sclog[5] = $sc[$i*$term + $j];
			}elsif(($sc[$i*$term + $j] <= $predist + 0.5) && ($sc[$i*$term + $j] > $predist + 0.0)){
				$sclognum[6]++;
				$sclog[6] = $sc[$i*$term + $j];
			}elsif(($sc[$i*$term + $j] <= $predist - 0.0) && ($sc[$i*$term + $j] > $predist - 1.0)){
				$sclognum[7]++;
				$sclog[7] = $sc[$i*$term + $j];
			}elsif(($sc[$i*$term + $j] <= $predist - 1.0) && ($sc[$i*$term + $j] > $predist - 5.0)){
				$sclognum[8]++;
				$sclog[8] = $sc[$i*$term + $j];
			}elsif(($sc[$i*$term + $j] <= $predist - 5.0) && ($sc[$i*$term + $j] > $predist - 20.0)){
				$sclognum[9]++;
				$sclog[9] = $sc[$i*$term + $j];
			}elsif(($sc[$i*$term + $j] <= $predist - 100.0)){
				$sclognum[10]++;
				$sclog[10] = $sc[$i*$term + $j];
		#	}elsif(($sc[$i*$term + $j] == -1068 + $maxd)){
		#		$sclognum[10]++;
		#		$sclog[10] = $sc[$i*$term + $j];
			}

		}

		$scat = $scat + $sclognum[10];
	
		# 標準出力
		for(my $l=1; $l<=10; $l++){
			print "$sclognum[$l], ";
		}

		# 積雪深決定
		for(my $k=2; $k<=9; $k++){
			if($sclognum[$k] > $threnum){
				# 増加
				if($k<7 && $decrease == 0){
					$predist = $sclog[$k];
					$decflag = 0;
					last;
				# 微妙？
				}elsif($k==7 || $k==8){
					last;
				# 減少
				}elsif($k==9 && $decflag == 1){
#					$predist = $predist-1;
					$decrease = 1;
					print "(decrease)";
					last;
				}
			}elsif($k == 9){
				$naflag = 1;
			}
		}


		# 変数に格納
		if($naflag == 1){
			push @termsc, "NA";
		}else{
			push @termsc, $predist;
		}
		push @termtime, $times[$i*$term];


		print " -> $termsc[$i]$ln";

	}


	# 補間

	my $namax = 0;
	my $prenacnt = 0;
	my @nacntarray;

	for(my $i=0; $i<=$#termsc; $i++){
		my $nacnt = 1;

		# 現在のデータがNAか
		if($termsc[$i] =~ m/NA/){
			while($nacnt<=$#termsc){
				# NAでないデータを探す
				if(!($termsc[$i+$nacnt] =~ m/NA/)){
					# 前回に引き続きNAかどうか判断
					if($prenacnt-1 != $nacnt){
						print "NA$nacnt <br>";
						push @nacntarray, $nacnt;
						if($nacnt > $namax){ $namax = $nacnt;}
					}
					$prenacnt = $nacnt;
					last;
				}
				$nacnt++;
			}
			if($i == 0 || $i + $nacnt -1 == $#termsc){
				$termsc[$i] = $predist;
			}else{
				$termsc[$i] = $termsc[$i-1] + ($termsc[$i+$nacnt]-$termsc[$i-1])/($nacnt+1);
			}
#			$termtime[$i] = $termtime[$i-1] + 60;
		}
		
#		print "$termtime[$i] :: $termsc[$i]$ln";

		$writeline = "$writeline$termtime[$i],$termsc[$i]$ln";


		# １０分平均積雪深、降雪深算出
		$avesc += $termsc[$i];
		if($decflag == 0){
			if($thermo < $thermothre){
				if($i != 0){
					if(($termsc[$i] - $termsc[$i-1]) > 0){
						$fall += $termsc[$i] - $termsc[$i-1];
					}
				}else{
					if(($termsc[$i] - $firstdist) > 0){ 
						$fall += $termsc[$i] - $firstdist;
					}
				}
			}
		}

	}

	$avesc = $avesc/($#termsc + 1);
if($decrease==1){ $avesc=$avesc-1;}
	$avesc = sprintf("%.1f", $avesc);
	print "avesc = $avesc , fall = $fall$ln";

	$wtime = $termtime[8];

	$fall = sprintf("%.1f", $fall);
	my $writefall = "$wtime,$fall$ln";	

	$scat = $scat / (9*$term);
	$scat = sprintf("%.2f", $scat);
	my $writescat = "$wtime,$scat,$fall$ln";
	print "scat = $scat$ln";	

#	writeFile($writeline, $writefall, $termsc[8], $writescat);
	writeFile($writeline, $writefall, $avesc, $writescat);
	changeXml();
}


# Webページ表示用XML整形部
sub changeXml{

	$locno--;
	($sec, $min, $hour, $mday, $mon, $year) = localtime($wtime);
	$year += 1900; $mon += 1;

	my $ref = XMLin($XML);

	$wtime = "$year/$mon/$mday $hour:$min:$sec";
	my @pretime = split(/:| /,$ref->{loc}[$locno]->{sctime});

	$ref->{loc}[$locno]->{time} = $wtime;

	if($hour > $pretime[1] || ($hour==0 && $pretime[1]==23)){
		
		for(my $j=24; $j>=1; $j--){
			my $k = $j-1;
			my $sctag = "sc$j";
			my $falltag = "fall$j";
			my $sctime = "sctime$j";
#			if($j == 1){
#				$ref->{loc}[$locno]->{$sctime}
#					 = $ref->{loc}[$locno]->{sctime};
#				$ref->{loc}[$locno]->{$sctag}
#					 = $ref->{loc}[$locno]->{sc};
#				$ref->{loc}[$locno]->{$falltag}
#					 = $ref->{loc}[$locno]->{fall0};
#			}else{
				my $presc = "sc$k";
				my $prefall = "fall$k";
				my $presctime = "sctime$k";
				$ref->{loc}[$locno]->{$sctime}
					 = $ref->{loc}[$locno]->{$presctime};
				$ref->{loc}[$locno]->{$sctag}
					 = $ref->{loc}[$locno]->{$presc};
				$ref->{loc}[$locno]->{$falltag}
					 = $ref->{loc}[$locno]->{$prefall};
#			}
		}
		$ref->{loc}[$locno]->{sctime0} = $wtime;
		$ref->{loc}[$locno]->{sc0} = $avesc;
		$ref->{loc}[$locno]->{fall0} = 0;
	}
	$ref->{loc}[$locno]->{sctime} = $wtime;
	$ref->{loc}[$locno]->{sc} = $avesc;
	$ref->{loc}[$locno]->{fall0} = ($ref->{loc}[$locno]->{fall0}+0)+$fall;
	$ref->{loc}[$locno]->{fall} = $fall;

	if(open(FH, "> $XML")){
		print "open $XML$ln";
		print FH XMLout($ref);
		print FH "\n";
		close(FH);
	}else{
		print "Error: Can't open $XML";
	}

#print Dumper($ref);

	print "$ln---curl end---$ln";
}


# データ書込み
sub writeFile{

	my @wlines = @_;

#	print "wline presc is $wlines[2]$ln sc is $ln$wlines[0]fall is $wlines[1]";
	print "wline presc is $wlines[2]$ln"; # sc is $ln$wlines[0]fall is $wlines[1]";
	
	# pre書込み
	if(open(P, "> $prefn")){
		flock(P, 2);
		print P "$wlines[2]";
		close P;
	}else{
		print "error: Can't open $prefn$ln";
	}

	# 1min積雪深書込み
#	if(open(F, ">> $outputfn")){
#		flock(F, 2);
#		print F "$wlines[0]";
#		close F;
#	}else{
#		print "error: Can't open $outputfn$ln";
#	}

	if(open(SC, ">> $outscfn")){
		flock(SC, 2);
		print SC "$wlines[0]";
		close SC;
	}else{
		print "error: Can't open $outscfn$ln";
	}

	# 降雪深書込み + 読み込み
	if(open(WF, ">> $outfall")){
		flock(WF, 2);
		print WF "$wlines[1]";
		close WF;
	}else{
		print "error: Can't open $outfall$ln";
	}

	if(open(WS, ">> $outscat")){
		flock(WS, 2);
		print WS "$wlines[3]";
		close WS;
	}else{
		print "error: Can't open $outscat$ln";
	}

#	print qq{saved as <a href="$outputfn">$outputfn</a>};
	print qq{saved in file<br>};

}


sub setpre{

	my $ref = XMLin($XML);
	$predist00 = $ref->{loc}[$locno-1]->{sc};
	$predist0 = $ref->{loc}[$locno-1]->{sc0};
	$predist1 = $ref->{loc}[$locno-1]->{sc1};
	if(($predist <= $predist00) && ($predist00 <= $predist0) && ($predist0 <= $predist1)){
		$decflag = 1;
		print "decflag=$decflag$ln";
	}

	$thermo = $ref->{loc}[$locno-1]->{thermo};
	print "set thermo=$thermo$ln";


	#読み込みファイル
	open my $FR, "<$prefn"
	  or die qq/fall : Cant open file : $!/;

	#ファイル読み込み
	while(my $line = <$FR>){
		$line =~ s/\r+\n//g;
		chomp($line);
		$predist = $line;
		$firstdist = $line;
		$predist = $predist + 0;
		$firstdist = $firstdist + 0;
   	}
	print "set predist = $predist$ln";

	if($predist == ""){
		print "can't set predist... $ln";
		$predist = $predist00;
	}

	close $FR;
}



