#!/usr/bin/perl
package MCalcModel;
use strict;

use Object;
use EventSource;

use PushOperator;
use DropOperator;
use SwapOperator;
use ClearHistoryOperator;
use AddOperator;
use SubtractOperator;
use MultiplyOperator;
use DivideOperator;

our @ISA = qw( EventSource );

sub new {
	my ($class, $cfg) = @_;
	my $self = $class->basic_new();
	$self->{_history} = [];
	$self->{_stack} = [];
	$self->initialize($cfg);
	$self->{_ops} = [
		#'\d+(?:\.\d*)?' => PushOperator->new($self),
		['\d+(\.\d*)?' => PushOperator->new($self)],
		['[dD]' => DropOperator->new($self)],
		['s' => SwapOperator->new($self)],
		['H' => ClearHistoryOperator->new($self)],
		#'[rds]' => $self->{unary_op},
		['\+' => AddOperator->new($self)],
		['-' => SubtractOperator->new($self)],
		['[*x]' => MultiplyOperator->new($self)],
		['/' => DivideOperator->new($self)],
		#'[%^*+/-]' => $self->{binary_op},
		[' ' => $self->{no_op}],
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
	$self->activate('pop-stack', $result, $self->{_stack});
	return $result;
}

sub clear_history {
	my ($self) = @_;
	printf "model - clear_history\n";
	$self->{_history} = [];
	$self->activate('history', $self->{_history});
}

sub get_stack {
	my ($self) = @_;
	return $self->{_stack};
}

sub get_history {
	my ($self) = @_;
	return $self->{_history};
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
			$op->apply($value);
			$ok = 1;
			last;
		}
		if (!$ok) {
			print "Failed to process input!\n";
			return;
		}
	}
}

1;
