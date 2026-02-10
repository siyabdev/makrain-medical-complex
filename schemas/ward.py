#Create Ward Request
class CreateWardRequest:
    def __init__(self, data):
        self.ward_name = data.get("ward_name")
        self.floor_number = data.get("floor_number")
    
    def is_valid(self):

        #Fields required
        if not all([self.ward_name, self.floor_number]):
            return False, "Missing required fields."
        
        return True, None

#Update Ward Request
class UpdateWardRequest:
    def __init__(self, data):
        self.id = data.get("id")
        self.ward_name = data.get("ward_name")
        self.floor_number = data.get("floor_number")
    
    def is_valid(self):

        if not self.id:
            return False, "Ward ID missing. Please provide ward ID."
        
        return True, None
    
    def has_any_updates(self):
        return any([self.ward_name, self.floor_number])
    
#Delete Ward Request
class DeleteWardRequest:
    def __init__(self, data):
        self.id = data.get("id")

    def is_valid(self):

        if not (self.id):
            return False, "Ward ID doesnt exist."
        
        return True, None

#Ward Response
class WardResponse:
    def __init__(self, data):
        self.id = data.id
        self.ward_name = data.ward_name
        self.floor_number = data.floor_number

    def is_valid(self):

        if not self.id:
            return False, "Ward ID missing. Please provide ward ID."
    
    def to_dict(self):
        return{
            "id": self.id,
            "ward_name": self.ward_name,
            "floor_number": self.floor_number
        }

#Ward List Response
class WardListResponse:
    def from_list(wards):
        return[WardResponse(war).to_dict() for war in wards]