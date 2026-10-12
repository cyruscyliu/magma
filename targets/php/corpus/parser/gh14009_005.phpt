<?php

trait T {
    private function test($s) {
        echo $s . " -> ". __CLASS__ . "::" . __METHOD__ . "\n";
    }
}

class A {
	use T;
	public function foo() {
		$this->test(__METHOD__);
	}
	public function bar() {
		$this->test(__METHOD__);
	}
}

class B extends A {
    use T;
	public function foo() {
		$this->test(__METHOD__);
	}
}

(new A)->foo();
(new A)->bar();
(new B)->foo();
(new B)->bar();
?>