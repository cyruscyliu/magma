<?php

class P {
    private function p(): void {}
}

class C extends P {
    #[\Override]
    public function p(): void {}
}

echo "Done";

?>