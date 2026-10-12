<?php

class Clazz {
	#[\NoDiscard]
	public function __clone() {
	}
}

$cls = new Clazz();

?>