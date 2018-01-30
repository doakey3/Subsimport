def get_base_strip(strip, base_strips):
    """Get the strip's base strip"""
    for i in range(len(base_strips)):
        if base_strips[i].frame_start <= strip.frame_start:
            if base_strips[i].frame_final_end >= strip.frame_final_end:
                return base_strips[i]