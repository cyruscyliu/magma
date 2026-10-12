<?php

class P {
	public $a = 'default';
	protected $b = 'default';
	private $c = 'default';
	public private(set) string $d = 'default';

	public function m1() {
		return clone($this, [ 'a' => 'updated A', 'b' => 'updated B', 'c' => 'updated C', 'd' => 'updated D' ]);
	}
}

class C extends P {
	public function m2() {
		return clone($this, [ 'a' => 'updated A', 'b' => 'updated B', 'c' => 'dynamic C' ]);
	}

	public function m3() {
		return clone($this, [ 'd' => 'inaccessible' ]);
	}
}

class Unrelated {
	public function m3(P $p) {
		return clone($p, [ 'b' => 'inaccessible' ]);
	}
}

$p = new P();

var_dump(clone($p, [ 'a' => 'updated A' ]));
var_dump($p->m1());

$c = new C();
var_dump($c->m1());
var_dump($c->m2());
try {
	var_dump($c->m3());
} catch (Error $e) {
	echo $e::class, ": ", $e->getMessage(), PHP_EOL;
}

try {
	var_dump(clone($p, [ 'b' => 'inaccessible' ]));
} catch (Error $e) {
	echo $e::class, ": ", $e->getMessage(), PHP_EOL;
}

try {
	var_dump(clone($p, [ 'd' => 'inaccessible' ]));
} catch (Error $e) {
	echo $e::class, ": ", $e->getMessage(), PHP_EOL;
}

try {
	var_dump((new Unrelated())->m3($p));
} catch (Error $e) {
	echo $e::class, ": ", $e->getMessage(), PHP_EOL;
}

?>