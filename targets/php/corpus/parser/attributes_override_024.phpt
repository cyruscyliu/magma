<?php

abstract class P {
    public abstract function __construct();
}

class C extends P {
    #[\Override]
    public function __construct() {}
}

echo "Done";

?>