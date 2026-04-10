<?php

class A {
	public string $foo;
}

class B extends A {
	public private(set) string $foo;
}

?>