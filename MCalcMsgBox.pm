#!/usr/bin/perl
package MCalcMsgBox;
use strict;

use Getopt::Long;
use Glib qw(TRUE FALSE);
use Gtk2 -init;

my %LEVEL_ICONS = (
	0 => 'error',
	1 => 'error',
	2 => 'warning',
	3 => 'info',
	4 => 'info',
	5 => 'info',
);
sub show_msgs {
	my ($class, $msgs, $continuation, $title) = @_;
	if (!@$msgs) {
		&$continuation(5);
	}

	my $level = 4;
	for my $a (@$msgs) {
		printf STDERR "%s (%d)\n", $$a[1], $$a[0];
		$level = $$a[0] if $$a[0] < $level;
	}

	my $wnd = Gtk2::Window->new("toplevel");
	$wnd->signal_connect("destroy" => sub {
		&$continuation($level);
	});

	my $a1 = Gtk2::Alignment->new(0.5, 0.5, 0.9, 0.9);
	$a1->set_padding(6, 6, 6, 6);
	$wnd->add($a1);

	my $v1 = Gtk2::VBox->new(FALSE, 6);
	$a1->add($v1);
	my $h1 = Gtk2::HBox->new(FALSE, 6);
	$v1->pack_start($h1, TRUE, FALSE, 0);

	my $img = Gtk2::Image->new_from_stock('gtk-dialog-' . $LEVEL_ICONS{$level}, 'GTK_ICON_SIZE_DIALOG');
	$h1->add($img);
	my $v2 = Gtk2::VBox->new(FALSE, 0);
	$h1->add($v2);

	for my $a(@$msgs) {
		my $lbl = Gtk2::Label->new($$a[1]);
		$v2->add($lbl);
	}

	my $a2 = Gtk2::Alignment->new(0.5, 0.5, 0.3, 0.1);
	$v1->pack_start($a2, FALSE, FALSE, 0);

	my $btn = Gtk2::Button->new_from_stock("gtk-ok");
	$btn->signal_connect("clicked" => sub {
		$wnd->destroy();
	});
	$a2->add($btn);

	$wnd->show_all();
	return $wnd;
}

1;
