<?php

#[DelayedTargetValidation]
#[SensitiveParameter] // Does nothing here
class DemoClass {
	#[DelayedTargetValidation]
	#[SensitiveParameter] // Does nothing here
	public $val;

	public string $hooked {
		#[DelayedTargetValidation]
		#[SensitiveParameter] // Does nothing here
		get => $this->hooked;
		#[DelayedTargetValidation]
		#[SensitiveParameter] // Does nothing here
		set => $value;
	}

	#[DelayedTargetValidation]
	#[SensitiveParameter] // Does nothing here
	public const CLASS_CONST = 'FOO';

	public function __construct(
		#[DelayedTargetValidation]
		#[SensitiveParameter] // Does something here
		$str
	) {
		echo "Got: $str\n";
		$this->val = $str;
	}

	#[DelayedTargetValidation]
	#[SensitiveParameter] // Does nothing here
	public function printVal(
		#[DelayedTargetValidation]
		#[SensitiveParameter]
		$sensitive // Does something here
	) {
		throw new Exception('Testing backtrace');
	}

}

#[DelayedTargetValidation]
#[SensitiveParameter] // Does nothing here
function demoFn() {
	echo __FUNCTION__ . "\n";
	return 456;
}

#[DelayedTargetValidation]
#[SensitiveParameter] // Does nothing here
const GLOBAL_CONST = 'BAR';

$d = new DemoClass('example');
var_dump($d->val);
$d->hooked = "foo";
var_dump($d->hooked);
var_dump(DemoClass::CLASS_CONST);
demoFn();
var_dump(GLOBAL_CONST);

$d->printVal('BAZ');


?>