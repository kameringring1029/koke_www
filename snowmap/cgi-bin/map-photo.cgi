#! /usr/bin/perl
use strict;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use POSIX qw(strftime);

my $q = new CGI;

print $q->header(), $q->start_html();
#print $q->dump; # for debug

my $outputdir = "/var/www/snowmap/log/photo";
my $fh = $q->param('uploaded_file');
my $no = $q->param('nolocation');

if ($fh ne ""){
	
	#my $ex = split(/./,$fh);
	my $name="photo$no";

	my ($ex) = ($fh =~ m|(\.[^./\\]+)$|);
	my $tag = $q->param('tag');
	$ex = $tag.$ex if ($tag ne "" and $tag =~ /^[A-Z0-9_-]+$/i);

	my $timestamp = strftime "%y_%m%d_%H%M", localtime;
	my $outputfn = "$outputdir/loc$no/today/$timestamp$ex";
	open(F, "> $outputfn") or die;
	my $outputfs = "$outputdir/loc$no/$name$ex";
	open(FS, "> $outputfs") or die;
	if (defined $fh) {
		while (<$fh>) {
			print F $_;
			print FS $_;
		}
	}
	close F;
	close FS;

	print qq{saved as <a href="$outputfn">$outputfn</a>};
  
}

$q->delete_all();

print qq(<p><a href="@{[$q->self_url]}">RELOAD</a></p>);

print $q->start_multipart_form(-name => 'myform'),
	"FILE", $q->filefield(-name => 'uploaded_file'),
	"no", $q->textfield(-name => 'nolocation'), $q->submit("OK"),
	$q->endform;

my @fl = reverse <$outputdir/[0-9]*>;
print "<ul>", (map {qq(<li><a href="$_" target="_blank">$_</a> (@{[-s $_]}))} @fl), "</ul>";

print $q->end_html(), "\n";


