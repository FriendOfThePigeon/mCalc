#!/usr/bin/perl
package UnaryOperator;
use strict;

use Operator;

our @ISA = qw( Operator );

sub apply {
	my ($self, $value) = @_;
	my $model = $self->{_model};
	my $value = $model->pop();
	if (!defined($value)) {
		return;
	}
	my $result = $self->unary_apply($value);
	$model->push_result($result);
}

1;
