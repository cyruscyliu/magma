<?php

class P {
    private mixed $p;
}

class C extends P {
    #[\Override]
    private mixed $p;
}

echo "Done";

?>