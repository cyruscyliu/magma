<?php

class Clazz {
	#[\Deprecated("prefix")]
	public const PREFIX = "prefix";

	#[\Deprecated("suffix")]
	public const SUFFIX = "suffix";

	public const CONSTANT = self::PREFIX . self::SUFFIX;
}

var_dump(Clazz::CONSTANT);

?>