#!/usr/bin/perl
package MCalcModel;
use strict;

use Object;
use EventSource;

use NoOperator;
use PushOperator;
use DropOperator;
use UndoOperator;
use SwapOperator;
use ClearHistoryOperator;
use AddOperator;
use SubtractOperator;
use MultiplyOperator;
use DivideOperator;
use PowerOperator;

our @ISA = qw( EventSource );

sub new {
	my ($class, $cfg) = @_;
	my $self = $class->basic_new();
	$self->{_history} = [];
	$self->{_stack} = [];
	$self->{_undoing} = 0;
	$self->{_undo} = [];
	$self->initialize($cfg);
	$self->{_ops} = [
		#'\d+(?:\.\d*)?' => PushOperator->new($self),
		['\d+(\.\d*)?' => PushOperator->new($self)],
		['[dD]' => DropOperator->new($self)],
		['u' => UndoOperator->new($self)],
		['s' => SwapOperator->new($self)],
		['H' => ClearHistoryOperator->new($self)],
		#'[rds]' => $self->{unary_op},
		['\+' => AddOperator->new($self)],
		['-' => SubtractOperator->new($self)],
		['[*x]' => MultiplyOperator->new($self)],
		['/' => DivideOperator->new($self)],
		['\^' => PowerOperator->new($self)],
		#'[%^*+/-]' => $self->{binary_op},
		[' ' => NoOperator->new($self)],
	];
	return $self;
}

sub initialize {
	my ($self, $cfg) = @_;
	$self->{_cfg} = ($cfg or {});
	return $self;
}

sub result {
	my ($self, $value) = @_;
	push @{ $self->{_history} }, $value;
	$self->activate('result', $value, $self->{_history});
}

sub push {
	my ($self, $value) = @_;
	push @{ $self->{_stack} }, $value;
	push @{ $self->{_undo} }, 'd' unless $self->{_undoing};
	$self->activate('push-stack', $value, $self->{_stack});
}

sub push_result {
	my ($self, $value) = @_;
	$self->result($value);
	$self->push($value);
}

sub pop {
	my ($self) = @_;
	my $result = pop @{ $self->{_stack} };
	push @{ $self->{_undo} }, $result unless $self->{_undoing};
	$self->activate('pop-stack', $result, $self->{_stack});
	return $result;
}

sub clear_history {
	my ($self) = @_;
	$self->{_history} = [];
	$self->activate('history', $self->{_history});
}

sub mark_command {
	my ($self) = @_;
	push @{ $self->{_undo} }, '';
}

sub get_stack {
	my ($self) = @_;
	return $self->{_stack};
}

sub get_history {
	my ($self) = @_;
	return $self->{_history};
}

sub undo {
	my ($self, $count) = @_;
	if ($self->{_undoing}) {
		printf STDERR "Already undoing!\n";
		return;
	}
	$self->{_undoing} = 1;
	if (!(defined $count)) {
		$count = 1;
	}
	printf STDERR "Undoing %d commands\n", $count;
	$count++; # First item is a mark for the undo command itself.
	while ($count > 0) {
		my $ok = 0;
		my $next = pop @{ $self->{_undo} };
		printf STDERR "Next to undo is >%s<\n", $next;
		if ($next eq '') {
			$count--;
			next;
		}
		for my $item (@{ $self->{_ops} }) {
			my ($exp, $op) = @$item;
			next unless $next =~ m/^($exp)$/;
			my $value = $1;
			$op->apply($value);
			$ok = 1;
			last;
		}
		if (!$ok) {
			print STDERR "Failed to process undo operation!\n";
			return;
		}
	}
	printf STDERR "Finished undoing\n";
	$self->{_undoing} = 0;
}

sub input {
	my ($self, $input) = @_;
	my $input = $input;
	while ($input ne '') {
		my $ok = 0;
		for my $item (@{ $self->{_ops} }) {
			my ($exp, $op) = @$item;
			next unless $input =~ m/( *($exp))/;
			my $value = $2;
			$input = substr($input, length($1));
			$self->mark_command();
			$op->apply($value);
			$ok = 1;
			last;
		}
		if (!$ok) {
			print STDERR "Failed to process input!\n";
			return;
		}
	}
}

1;
