<?php

#[DelayedTargetValidation]
#[NoDiscard]
class Demo {

	#[DelayedTargetValidation]
	#[Attribute]
	public const FOO = 'BAR';

	#[DelayedTargetValidation]
	#[Attribute]
	public string $v1;

	public string $v2 {
		#[DelayedTargetValidation]
		#[Attribute]
		get => $this->v2;
		#[DelayedTargetValidation]
		#[Attribute]
		set => $value;
	}

	#[DelayedTargetValidation]
	#[Attribute]
	public function __construct(
		#[DelayedTargetValidation]
		#[Attribute]
		public string $v3
	) {
		$this->v1 = $v3;
		echo __METHOD__ . "\n";
	}
}

#[DelayedTargetValidation]
#[Attribute]
function demoFn() {
	echo __FUNCTION__ . "\n";
}

#[DelayedTargetValidation]
#[Attribute]
const EXAMPLE = true;

$cases = [
	new ReflectionClass('Demo'),
	new ReflectionClassConstant('Demo', 'FOO'),
	new ReflectionProperty('Demo', 'v1'),
	new ReflectionProperty('Demo', 'v2')->getHook(PropertyHookType::Get),
	new ReflectionProperty('Demo', 'v2')->getHook(PropertyHookType::Set),
	new ReflectionMethod('Demo', '__construct'),
	new ReflectionParameter([ 'Demo', '__construct' ], 'v3'),
	new ReflectionProperty('Demo', 'v3'),
	new ReflectionFunction('demoFn'),
	new ReflectionConstant('EXAMPLE'),
];
foreach ($cases as $r) {
	echo str_repeat("*", 20) . "\n";
	echo $r . "\n";
	$attributes = $r->getAttributes();
	var_dump($attributes);
	try {
		$attributes[1]->newInstance();
	} catch (Error $e) {
		echo get_class($e) . ": " . $e->getMessage() . "\n";
	}
}

?>