<?php
class Tmp {
	public function __toString() {
		return "abc";
	}
}

$tmp = new Tmp;
$tmp .= $tmp;
echo $tmp . "\n";
?>