#!/usr/bin/perl
package Operator;
use strict;

use Object;

our @ISA = qw( Object );

sub new {
	my ($class, $model, @args) = @_;
	my $self  = $class->basic_new()->initialize($model, @args);
	return $self;
}

sub initialize {
	my ($self, $model, @args) = @_;
	$self->{_model} = $model;
	return $self;
}

sub apply {
	my ($self) = @_;
}

1;
