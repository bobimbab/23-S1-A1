from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import Layer
from data_structures.queue_adt import CircularQueue
from data_structures.set_adt import Set


class LayerStore(ABC):

    def __init__(self) -> None:
        pass
        

    @abstractmethod
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        pass

    @abstractmethod
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        pass

class SetLayerStore(LayerStore):
    """
    Set layer store. A single layer can be stored at a time (or nothing at all)
    - add: Set the single layer.
    - erase: Remove the single layer. Ignore what is currently selected.
    - special: Invert the colour output.
    """
    def __init__(self):
        super().__init__()
        self.layer = None
        self.special_mode = False
        
    def add(self, layer: Layer) -> bool:
        if layer != self.layer:
            self.layer = layer
            return True
        return False
    
    def erase(self, layer: Layer) -> bool:
        self.layer = None
        return True
        
    
    def special(self):
        self.special_mode = not self.special_mode
        
    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        r, g, b = (0, 0, 0)
        if self.layer is not None:
            return self.layer.apply(start, timestamp, x, y)
        elif self.special_mode == True:
            self.layer = 
            return self.layer.apply(start, timestamp, x, y)
        else:
            return start

class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """
    def __init__(self, max_layers: int) -> None:
        super().__init__()
        self.layers = CircularQueue(capacity)
    
    def add(self, layer: Layer) -> bool:
        if self.layers.is_full():
            return False
        self.layers.append(layer)
        return True
    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        r, g, b, a = 0, 0, 0, 0

        for layer in self.layers:
            if layer.start <= start and layer.end >= timestamp:
                pixel = layer.get_pixel(start, timestamp, x, y)
                r += pixel[0]
                g += pixel[1]
                b += pixel[2]
                a += pixel[3]

        if a == 0:
            return 0, 0, 0
        else:
            r, g, b = r // a, g // a, b // a
            return r, g, b
    
    def erase(self, layer: Layer) -> bool:
        if self.layers.is_empty():
            return False
        layer == self.layers.serve()
        return True
        
    def special(self):
        layers = []
        while not self.layers.is_empty():
            layers.append(self.layers.serve())
            layers.reverse()
         
        for layer in layers:
            self.layers.append(layer)

class SequenceLayerStore(LayerStore):
    """
    Sequential layer store. Each layer type is either applied / not applied, and is applied in order of index.
    - add: Ensure this layer type is applied.
    - erase: Ensure this layer type is not applied.
    - special:
        Of all currently applied layers, remove the one with median `name`.
        In the event of two layers being the median names, pick the lexicographically smaller one.
    """
    def __init__(self) -> None:
        super().__init__()
        self.applied_layers = set()

    def add(self, layer: Layer) -> bool:
        if layer.name not in self.applied_layers:
            self.applied_layers.add(layer.name)
            return True
        else:
            return False

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        color = start
        for layer in self.applied_layers:
            if layer.name in self.applied_layers:
                color = layer.apply(start, timestamp, x, y, color)
        return color

    def erase(self, layer: Layer) -> bool:
        self.applied_layers.remove(layer.name)
        return True

    def special(self):
        median_name = sorted(self.applied_layers)[len(self.applied_layers) // 2]
        self.applied_layers.remove(median_name)