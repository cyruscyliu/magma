<?php

class DemoClass {

	public string $hooked {
		get => $this->hooked;
		#[DelayedTargetValidation]
		#[Override] // Does something here
		set => $value;
	}
}

?>