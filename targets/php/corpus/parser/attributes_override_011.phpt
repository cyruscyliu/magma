<?php

class P {
    private function p(): void {}
}

class C extends P {
    #[\Override]
    private function p(): void {}
}

echo "Done";

?>