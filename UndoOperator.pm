#!/usr/bin/perl
package UndoOperator;
use strict;

use Operator;

our @ISA = qw( Operator );

sub apply {
	my ($self, $exp) = @_;
	my $model = $self->{_model};
	my $value = $model->undo();
}

1;
