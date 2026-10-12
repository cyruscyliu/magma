<?php

class DemoClass {

	public string $hooked {
		#[DelayedTargetValidation]
		#[Override] // Does something here
		get => $this->hooked;
		set => $value;
	}
}

?>