<?php

class Clazz {
	public string $test {
		#[\NoDiscard]
		set(string $value) {
			$this->test = $value;
		}
	}
}

$cls = new Foo();
$cls->test = 'foo';

?>