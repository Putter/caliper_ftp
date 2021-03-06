#!/usr/bin/perl

use strict;

# don't use warnings module as it is not portable enough
# use warnings;

my $header_name = '_PROTO_H_';

if ($ARGV[0] eq '-h') {
	shift @ARGV;
	$header_name = shift @ARGV;
}

sub print_header {
	print "#ifndef $header_name\n";
	print "#define $header_name\n\n";
	print "/* This file is automatically generated with \"make proto\". DO NOT EDIT */\n\n";
}

sub print_footer {
	printf "\n#endif /*  %s  */\n", $header_name;
}


sub handle_loadparm {
	my $line = shift;

	if ($line =~ /^FN_(GLOBAL|LOCAL)_(CONST_STRING|STRING|BOOL|CHAR|INTEGER|LIST)\((\w+),.*\)/o) {
		my $scope = $1;
		my $type = $2;
		my $name = $3;

		my %tmap = (
			    "BOOL" => "BOOL ",
			    "CONST_STRING" => "const char *",
			    "STRING" => "const char *",
			    "INTEGER" => "int ",
			    "CHAR" => "char ",
			    "LIST" => "const char **",
			    );

		my %smap = (
			    "GLOBAL" => "void",
			    "LOCAL" => "int "
			    );

		print "$tmap{$type}$name($smap{$scope});\n";
	}
}


sub process_file($) 
{
	my $filename = shift;

	open(FH, "< $filename") || die "Failed to open $filename";

	print "\n/* The following definitions come from $filename  */\n\n";

	while (my $line = <FH>) {	      
		# these are ordered for maximum speed
		next if ($line =~ /^\s/);
	      
		next unless ($line =~ /\(/);

		next if ($line =~ /^\/|[;]/);

		next unless ( $line =~ /
			      ^void|^BOOL|^int|^struct|^char|^const|^\w+_[tT]\s|^uint|^unsigned|^long|
			      ^NTSTATUS|^ADS_STATUS|^enum\s.*\(|^DATA_BLOB|^WERROR|^XFILE|^FILE|^DIR|
			      ^double|^TDB_CONTEXT|^TDB_DATA|^TALLOC_CTX|^NTTIME|^FN_|^REG_KEY|^REG_HANDLE|^REG_VAL|
			      ^GtkWidget|^GType|^smb_ucs2_t
			      /xo);

		next if ($line =~ /^int\s*main/);

		if ($line =~ /^FN_/) {
			handle_loadparm($line);
			next;
		}

		if ( $line =~ /\(.*\)\s*$/o ) {
			chomp $line;
			print "$line;\n";
			next;
		}

		print $line;

		while ($line = <FH>) {
			if ($line =~ /\)\s*$/o) {
				chomp $line;
				print "$line;\n";
				last;
			}
			print $line;
		}
	}

	close(FH);
}

sub process_files {
	foreach my $filename (@ARGV) {
		process_file($filename);
	}
}

print_header();
process_files();
print_footer();
