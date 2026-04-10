<?php

class DemoClass {

	#[DelayedTargetValidation]
	#[Override] // Does something here
	public function printVal() {
		echo 'Value is: ' . $this->val . "\n";
		return 123;
	}
}

?>