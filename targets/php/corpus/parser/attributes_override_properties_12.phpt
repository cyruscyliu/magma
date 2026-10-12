<?php

class P {
    protected mixed $p;
}

class C extends P {
    #[\Override]
    protected mixed $p;
}

echo "Done";

?>