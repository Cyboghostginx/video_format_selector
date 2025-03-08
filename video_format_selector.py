import torch
import os
import folder_paths
import comfy.utils

class VideoFormatSelector:
    """
    Custom node for WAN video generation that exactly mimics EmptyHunyuanLatentVideo.
    Based on careful analysis of the original workflow structure.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "format": ([
                    "Landscape - 16:9 (480p)",
                    "Landscape - 16:9 (720p)",
                    "Portrait - 9:16 (480p)",
                    "Portrait - 9:16 (720p)",
                    "Square - 1:1 (512px)",
                    "Square - 1:1 (768px)"
                ], {"default": "Landscape - 16:9 (480p)"}),
                "frames": ("INT", {"default": 33, "min": 1, "max": 240, "step": 1}),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 4, "step": 1})
            }
        }
    
    RETURN_TYPES = ("LATENT",)
    FUNCTION = "get_format"
    CATEGORY = "latent"  # Match the same category as EmptyHunyuanLatentVideo
    
    def get_format(self, format, frames, batch_size):
        # Preset dimensions based on format selection
        presets = {
            "Landscape - 16:9 (480p)": (832, 480),
            "Landscape - 16:9 (720p)": (1280, 720),
            "Portrait - 9:16 (480p)": (480, 832),
            "Portrait - 9:16 (720p)": (720, 1280),
            "Square - 1:1 (512px)": (512, 512),
            "Square - 1:1 (768px)": (768, 768)
        }
        
        # Select dimensions from presets
        width, height = presets.get(format, (832, 480))
        
        # Ensure dimensions are divisible by 8 (VAE requirement)
        width = width - (width % 8)
        height = height - (height % 8)
        
        # Create empty latent tensor with appropriate dimensions
        # Match EXACTLY the same structure as EmptyHunyuanLatentVideo
        latent = torch.zeros([batch_size, 4, height // 8, width // 8])
        
        print(f"VideoFormatSelector: Creating {width}x{height} video with {frames} frames ({frames/24:.2f} seconds at 24fps)")
        
        # Match the exact EmptyHunyuanLatentVideo return structure
        return ({"samples": latent, "frames": frames},)

# Direct drop-in replacement for EmptyHunyuanLatentVideo
class EmptyWANLatentVideo:
    """
    Direct replacement for EmptyHunyuanLatentVideo with identical interface.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "width": ("INT", {"default": 832, "min": 256, "max": 2048, "step": 8}),
                "height": ("INT", {"default": 480, "min": 256, "max": 2048, "step": 8}),
                "frames": ("INT", {"default": 33, "min": 1, "max": 240, "step": 1}),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 4, "step": 1})
            }
        }
    
    RETURN_TYPES = ("LATENT",)
    FUNCTION = "generate"
    CATEGORY = "latent"
    
    def generate(self, width, height, frames, batch_size):
        latent = torch.zeros([batch_size, 4, height // 8, width // 8])
        print(f"EmptyWANLatentVideo: Creating {width}x{height} video with {frames} frames ({frames/24:.2f} seconds at 24fps)")
        return ({"samples": latent, "frames": frames},)

# Simple info node for video format information
class VideoFormatInfo:
    """
    Provides information about video formats and duration.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "frames": ("INT", {"default": 120, "min": 1, "max": 240, "step": 1})
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "get_info"
    CATEGORY = "utils"
    
    def get_info(self, frames):
        seconds = frames / 24
        
        # Calculate common frame counts
        common_durations = {
            "1 second": 24,
            "2 seconds": 48,
            "3 seconds": 72,
            "5 seconds": 120,
            "10 seconds": 240
        }
        
        info = f"Frame Information:\n\n"
        info += f"{frames} frames = {seconds:.2f} seconds at 24fps\n\n"
        info += "Common durations:\n"
        
        for duration, frame_count in common_durations.items():
            info += f"- {duration}: {frame_count} frames\n"
        
        return (info,)

# Add nodes to ComfyUI
NODE_CLASS_MAPPINGS = {
    "VideoFormatSelector": VideoFormatSelector,
    "EmptyWANLatentVideo": EmptyWANLatentVideo,
    "VideoFormatInfo": VideoFormatInfo
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VideoFormatSelector": "📽️ Video Format Selector",
    "EmptyWANLatentVideo": "🎬 Empty WAN Video Latent",
    "VideoFormatInfo": "⏱️ Video Duration Calculator"
}
