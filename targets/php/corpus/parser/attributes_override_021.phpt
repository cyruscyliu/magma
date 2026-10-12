<?php

class P {
    public function __construct() {}
}

class C extends P {
    #[\Override]
    public function __construct() {}
}

echo "Done";

?>