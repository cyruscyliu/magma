<?php

class Clazz {
	#[\Deprecated(self::TEST)]
	public const TEST = "from itself";

	#[\Deprecated]
	public const TEST2 = "from another";

	#[\Deprecated(self::TEST2)]
	public const TEST3 = 1;
}

Clazz::TEST;
Clazz::TEST3;

?>