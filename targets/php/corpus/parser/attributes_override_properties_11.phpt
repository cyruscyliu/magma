<?php

class P {
    protected mixed $p;
}

class C extends P {
    #[\Override]
    public mixed $p;
}

echo "Done";

?>