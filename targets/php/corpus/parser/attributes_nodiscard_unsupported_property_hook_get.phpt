<?php

class Clazz {
	public string $test {
		#[\NoDiscard]
		get {
			return 'asd';
		}
	}
}

$cls = new Clazz();
$cls->test;

?>