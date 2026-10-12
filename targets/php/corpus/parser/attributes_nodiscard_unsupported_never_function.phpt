<?php

#[\NoDiscard]
function test(): never {
	throw new \Exception('Error!');
}

test();

?>