<?php

class Clazz {
	public string $hooked = 'default' {
		set {
			$this->hooked = strtoupper($value);
		}
	}
}

$c = new Clazz();

var_dump(clone($c, [ 'hooked' => 'updated' ]));

?>