<?php
trait T {
	/** some doc */
	static protected $a = 0;
}
class A {
	/** some doc */
	static protected $a = 0;
}
class B extends A {
	use T;
}
?>
===DONE===