<?php

class WithoutAttrib implements Countable {
	public function count() {
		return 5;
	}
}

#[DelayedTargetValidation]
#[ReturnTypeWillChange] // Does nothing here
class DemoClass implements Countable {
	#[DelayedTargetValidation]
	#[ReturnTypeWillChange] // Does nothing here
	public $val;

	public string $hooked {
		#[DelayedTargetValidation]
		#[ReturnTypeWillChange] // Does nothing here
		get => $this->hooked;
		#[DelayedTargetValidation]
		#[ReturnTypeWillChange] // Does nothing here
		set => $value;
	}

	#[DelayedTargetValidation]
	#[ReturnTypeWillChange] // Does nothing here
	public const CLASS_CONST = 'FOO';

	public function __construct(
		#[DelayedTargetValidation]
		#[ReturnTypeWillChange] // Does nothing here
		$str
	) {
		echo "Got: $str\n";
		$this->val = $str;
	}

	#[DelayedTargetValidation]
	#[ReturnTypeWillChange] // Does something here
	public function printVal() {
		echo 'Value is: ' . $this->val . "\n";
	}

	#[DelayedTargetValidation]
	#[ReturnTypeWillChange] // Does something here
	public function count() {
		return 5;
	}
}

#[DelayedTargetValidation]
#[ReturnTypeWillChange] // Does nothing here
function demoFn() {
	echo __FUNCTION__ . "\n";
	return 456;
}

#[DelayedTargetValidation]
#[ReturnTypeWillChange] // Does nothing here
const GLOBAL_CONST = 'BAR';

$d = new DemoClass('example');
$d->printVal();
var_dump($d->val);
$d->hooked = "foo";
var_dump($d->hooked);
var_dump(DemoClass::CLASS_CONST);
demoFn();
var_dump(GLOBAL_CONST);
?>