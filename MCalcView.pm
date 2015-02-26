#!/usr/bin/perl
package MCalcView;
use strict;

use Glib qw(TRUE FALSE);
use Gtk2 -init;
use Gtk2::SimpleList;

use Object;

our @ISA = qw( Object );

sub new {
	my ($class, $params) = @_;
	my $self  = $class->basic_new()->initialize();
	$self->make_window();
	return $self;
}

sub initialize {
	my ($self) = @_;
	return $self;
}

sub set_show_msg {
	my ($self, $proc) = @_;
	$self->{_msg} = $proc;
	return $self;
}

sub set_abort {
	my ($self, $proc) = @_;
	$self->{_abort} = $proc;
	return $self;
}

sub set_model {
	my ($self, $model) = @_;
	$self->{_model} = $model;
	$model->add_listener($self);
	$self->event($model, 'all');
	return $self;
}

sub show {
	my ($self) = @_;
	$self->{_wnd}->show_all();
	return $self;
}

sub set_auto {
	my ($self, $on) = @_;
	if ($on) {
		$self->{_auto}++;
	} elsif ($self->{_auto} > 0) {
		$self->{_auto}--;
	}
}

sub on_auto {
	my ($self) = @_;
	return $self->{_auto} > 0;
}

sub list_entry_selected {
	my ($self, $sl, $selection) = @_;
	my ($model, $iter) = $selection->get_selected();
	if ($iter) {
		my $description = $model->get($iter, 0);
		$self->set_auto(1);
		$self->{_entry}->set_text($description);
		$self->set_auto(0);
	}
}

sub clear_entry {
	my ($self) = @_;
	$self->set_auto(1);
	$self->{_entry}->set_text('');
	$self->set_auto(0);
}

sub set_entry {
	my ($self, $text) = @_;
	$self->set_auto(1);
	$self->{_entry}->set_text($text);
	$self->set_auto(0);
}

sub send_to_model {
	my ($self, $input) = @_;
	return 0 if $self->on_auto();
	$self->set_auto(1);
	$self->clear_entry();
	$self->{_model}->input($input);
	$self->set_auto(0);
}

sub enter_activated {
	my ($self, $btn) = @_;
	return 0 if $self->on_auto();
	$self->send_to_model($self->{_entry}->get_text());
}

sub entry_edited {
	my ($self, $entry) = @_;
	return 0 if $self->on_auto();
	my $text = $self->{_entry}->get_text();
	if ($text =~ m/[^\d\.]$/) {
		$self->send_to_model($text);
	}
}

sub make_window {
	my ($self) = @_;

	my $wnd = Gtk2::Window->new("toplevel");
	$wnd->set_title('mtimes');
	$wnd->set_default_size(250, 300);

	my $cancel_handler = sub {
		my $model = $self->{_model};
		$wnd->destroy();
		$self->{_abort}->();
	};
	$wnd->signal_connect("delete_event" => $cancel_handler);

	my $a1 = Gtk2::Alignment->new(0.5, 0.5, 0.9, 0.9);
	$a1->set_padding(1, 1, 1, 1);
	$wnd->add($a1);

	my $vbox;
	$vbox = Gtk2::VBox->new(FALSE, 9);
	$a1->add($vbox);

	my $hbox1;
	$hbox1 = Gtk2::HBox->new(FALSE, 9);
	$vbox->pack_start($hbox1, TRUE, TRUE, 0);

	my $scroll1 = Gtk2::ScrolledWindow->new();
	$hbox1->pack_end($scroll1, TRUE, TRUE, 0);

	my $list1;
	$list1 = Gtk2::SimpleList->new('History' => 'text');
	my $select_handler = sub {
		my ($source) = @_;
		$self->list_entry_selected($list1, $source);
	};
	$list1->get_selection->signal_connect (changed => $select_handler);
	my $a2 = Gtk2::Alignment->new(0, 1, 1, 0);
	$a2->add($list1);
	$scroll1->add_with_viewport($a2);
	$self->{_history} = $list1;
	$self->{_history_scroll} = $scroll1;

	my $scroll2 = Gtk2::ScrolledWindow->new();
	$hbox1->pack_end($scroll2, TRUE, TRUE, 0);

	my $list2;
	$list2 = Gtk2::SimpleList->new('Stack' => 'text');
	my $select_handler = sub {
		my ($source) = @_;
		$self->list_entry_selected($list2, $source);
	};
	$list2->get_selection->signal_connect (changed => $select_handler);
	my $a3 = Gtk2::Alignment->new(0, 1, 1, 0);
	$a3->add($list2);
	$scroll2->add_with_viewport($a3);
	$self->{_stack} = $list2;
	$self->{_stack_scroll} = $scroll2;

	my $hbox2;
	$hbox2 = Gtk2::HBox->new(FALSE, 9);
	$vbox->pack_start($hbox2, FALSE, TRUE, 0);

	my $entry;
	$entry = Gtk2::Entry->new();
	my $edited_handler = sub {
		my ($source) = @_;
		$self->entry_edited($source);
	};
	for my $sig ('changed') {
		$entry->signal_connect($sig => $edited_handler);
	}
	$entry->set_property('activates-default' => 1);
	$hbox2->pack_start($entry, TRUE, TRUE, 0);
	$self->{_entry} = $entry;

	my $change_btn = Gtk2::Button->new_with_label("Enter");
	my $change_handler = sub {
		my ($source) = @_;
		$self->enter_activated($source);
	};
	$change_btn->signal_connect("clicked" => $change_handler);
	$hbox2->pack_start($change_btn, FALSE, TRUE, 0);
	$self->{_change_button} = $change_btn;
	$change_btn->set_flags('GTK_CAN_DEFAULT');
	$change_btn->grab_default();

	$self->{_wnd} = $wnd;
}

sub populate_list {
	my ($self, $list, $items, $scroll) = @_;
	my $list_data = $self->{$list}->{data};
    @$list_data = ( ); # Empty list
	for my $item (@$items) {
		push @$list_data, [ $item ];
	}
	if ($scroll) {
		my $sw = $self->{"${list}_scroll"};
		my $adj = $sw->get_vadjustment();
		$adj->set_value($adj->upper);
	}
}

sub append_list {
	my ($self, $list, $item, $scroll) = @_;
	my $list_data = $self->{$list}->{data};
	push @$list_data, [ $item ];
	if ($scroll) {
		my $sw = $self->{"${list}_scroll"};
		my $adj = $sw->get_vadjustment();
		$adj->set_value($adj->upper);
	}
}

sub update {
	my ($self) = @_;
	$self->set_auto(1);
	$self->populate_list('_stack', $self->{_model}->get_stack(), 1);
	$self->clear_entry();
	$self->set_auto(0);
}

sub update_result {
	my ($self, $result) = @_;
	$self->set_auto(1);
	$self->append_list('_history', $result, 1);
	$self->set_auto(0);
}

sub update_history {
	my ($self, $history) = @_;
	print "Updating history\n";
	$self->set_auto(1);
	$self->populate_list('_history', $self->{_model}->get_history(), 1);
	$self->set_auto(0);
}


sub push_stack {
	my ($self) = @_;
	$self->update();
}

sub pop_stack {
	my ($self, $value) = @_;
	$self->update();
}

sub event {
	my ($self, $source, $aspect, @data) = @_;
	if ($source == $self->{_model}) {
		if ($aspect eq 'history') {
			$self->update_history($data[0]);
		} elsif ($aspect eq 'stack') {
			#$self->populate_list('_stack', \@data);
		} elsif ($aspect eq 'push-stack') {
			$self->push_stack();
		} elsif ($aspect eq 'result') {
			$self->update_result($data[0]);
		} elsif ($aspect eq 'pop-stack') {
			$self->pop_stack($data[0]);
		}
	}
}

1;
