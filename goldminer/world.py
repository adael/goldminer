import random
from goldminer import settings, pgc, game, geom, texts, sound
from goldminer.camera import Camera
from goldminer.actor import Actor
from goldminer.worldmap import WorldMap


class World:
    def __init__(self, world_map: WorldMap, player: Actor, seed):
        self.world_map = world_map
        self.actors = []
        self.player = player
        self.player.world = self
        self.seed = seed

        self.camera = Camera(
            width=settings.map_rect.w,
            height=settings.map_rect.h,
            map_width=self.world_map.width,
            map_height=self.world_map.height,
            offset_x=settings.map_rect.x,
            offset_y=settings.map_rect.y
        )
        self.camera.update(self.player.x, self.player.y)
        self.stored_player_position = None

    def inside_map(self, x, y):
        return self.world_map.inside_map(x, y)

    def tile(self, x, y):
        return self.world_map.tile(x, y)

    def set_tile(self, x, y, tile):
        self.world_map.set_tile(x, y, tile)

    def add(self, actor):
        actor.set_world(self)
        self.actors.append(actor)
        return actor

    def is_walkable(self, x, y):
        return self.world_map.is_walkable(x, y)

    def actor_move(self, actor, x, y):
        (dx, dy) = actor.x + x, actor.y + y

        if self.is_walkable(dx, dy):
            actor.move(x, y)

    def player_move(self, x, y):

        if self.player.resting:
            return

        (dx, dy) = self.player.x + x, self.player.y + y

        self.player.orientation = (x, y)

        if self.is_walkable(dx, dy):
            self.player.move(x, y)
            # Currently fov is computed in each logic update
            # self.compute_fov()
            return

        tile = self.tile(dx, dy)
        if tile.door:
            if tile.door.opened:
                if tile.door.leave:
                    self.leave_room()
                else:
                    self.enter_room(dx, dy)
            else:
                self.player.see("{0} ({1})".format("a door", "closed" if tile.door.closed else "opened"))
        elif tile.resource:
            self.player.see("{0} ({1})".format(tile.resource.item.description, tile.resource.quantity))

    def player_primary_action(self):
        (x, y) = self.player.looking_position()
        tile = self.tile(x, y)
        if tile.resource:
            self.player_gather_resource(tile)
        elif tile.door:
            self.player_handle_door(tile, x, y)

    def player_handle_door(self, tile, dx, dy):
        if tile.door.closed:
            tile.door.open()
        else:
            tile.door.close()

    def player_gather_resource(self, tile):

        if self.player.inventory.is_full():
            self.player.think(texts.inventory_is_full)
            return

        sound.pick_axe.play()
        tile.resource.health -= 1
        self.player.waste(tile.resource.hardness)

        if tile.resource.health <= 0:
            if tile.resource.item:
                self.player.inventory.add(tile.resource.item)

            if tile.resource.quantity > 0:
                tile.resource.quantity -= 1
                tile.resource.restore_health()

        if tile.resource.depleted:
            self.player.think("This resource is depleted")
            tile.resource = None

    def actor_heal(self, actor, amount):
        actor.heal(amount)

    def actor_say(self, actor, messages):
        if actor is self.player or actor.distance_to(self.player) < 10:
            self.player.listen(actor.name + " says: " + random.choice(messages))

    def logic(self):
        if self.player.resting:
            self.player.think("Zzz ...")
            self.player.restore()
        self.camera.update(self.player.x, self.player.y)

    def enter_room(self, x, y):
        self.stored_player_position = self.player.position
        (dox, doy) = geom.orientation(self.player.x, self.player.y, x, y)

        print("Door orientation:", (dox, doy))

        hseed = "room_{}x{}_{}".format(x, y, self.seed)
        (house, door_x, door_y) = pgc.create_house(hseed, dox, doy)

        self.player.set_position(door_x - dox, door_y - doy)
        new_world = World(house, self.player, hseed)
        game.get_game_state().enter_world(new_world)

    def leave_room(self):
        game.get_game_state().leave_world()

    def restore_player_position(self):
        self.player.position = self.stored_player_position

    def compute_fov(self):
        positions = geom.positions_in_radius(self.player.x, self.player.y, 6)
        for (x, y) in positions:
            if self.world_map.inside_map(x, y):
                tile = self.tile(x, y)
                dist = self.player.distance(x, y)
                tile.in_sight = dist < 4

    def place_item(self, x, y, item):
        self.tile(x, y).place_item(item)
