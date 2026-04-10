<?php

class P {
    private mixed $p;
}

class C extends P {
    #[\Override]
    public mixed $p;
}

echo "Done";

?>