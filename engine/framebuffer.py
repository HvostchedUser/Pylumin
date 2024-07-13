import OpenGL.GL as gl

class Framebuffer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.framebuffer = gl.glGenFramebuffers(1)
        self.texture = gl.glGenTextures(1)
        self.renderbuffer = gl.glGenRenderbuffers(1)
        self.setup_framebuffer()

    def setup_framebuffer(self):
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.framebuffer)

        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.width, self.height, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, None)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, gl.GL_COLOR_ATTACHMENT0, gl.GL_TEXTURE_2D, self.texture, 0)

        gl.glBindRenderbuffer(gl.GL_RENDERBUFFER, self.renderbuffer)
        gl.glRenderbufferStorage(gl.GL_RENDERBUFFER, gl.GL_DEPTH24_STENCIL8, self.width, self.height)
        gl.glFramebufferRenderbuffer(gl.GL_FRAMEBUFFER, gl.GL_DEPTH_STENCIL_ATTACHMENT, gl.GL_RENDERBUFFER, self.renderbuffer)

        if gl.glCheckFramebufferStatus(gl.GL_FRAMEBUFFER) != gl.GL_FRAMEBUFFER_COMPLETE:
            raise RuntimeError('Framebuffer is not complete')

        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)

    def bind(self):
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.framebuffer)

    def unbind(self):
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)

    def cleanup(self):
        gl.glDeleteFramebuffers(1, [self.framebuffer])
        gl.glDeleteTextures(1, [self.texture])
        gl.glDeleteRenderbuffers(1, [self.renderbuffer])
