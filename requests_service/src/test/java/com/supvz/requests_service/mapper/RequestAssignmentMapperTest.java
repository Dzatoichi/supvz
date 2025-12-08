//package com.supvz.requests_service.mapper;
//
//import com.supvz.requests_service.core.enums.AssignmentAction;
//import com.supvz.requests_service.mapper.action.ActionMapper;
//import com.supvz.requests_service.model.dto.PageDto;
//import com.supvz.requests_service.model.dto.RequestAssignmentDto;
//import com.supvz.requests_service.model.dto.RequestAssignmentPayload;
//import com.supvz.requests_service.model.dto.RequestAssignmentUpdatePayload;
//import com.supvz.requests_service.model.entity.Request;
//import com.supvz.requests_service.model.entity.RequestAssignment;
//import org.junit.jupiter.api.BeforeEach;
//import org.junit.jupiter.api.Test;
//import org.junit.jupiter.api.extension.ExtendWith;
//import org.mockito.Mock;
//import org.mockito.junit.jupiter.MockitoExtension;
//import org.springframework.data.domain.Page;
//import org.springframework.data.domain.PageImpl;
//
//import java.time.LocalDateTime;
//import java.util.List;
//
//import static org.junit.jupiter.api.Assertions.*;
//import static org.mockito.Mockito.*;
//
//@ExtendWith(MockitoExtension.class)
//class RequestAssignmentMapperTest {
//    private RequestAssignmentEntityMapper target;
//    @Mock
//    private ActionMapper actionMapper;
//    @Mock
//    private AssignmentAction action;
//
//    @BeforeEach
//    public void setUp() {
//        List<ActionMapper> mappersList = List.of(actionMapper);
//        lenient().when(actionMapper.getType()).thenReturn(action);
//        target = new RequestAssignmentEntityMapper(mappersList);
//    }
//
//    @Test
//    void create__MapsPayloadToEntity() {
//        long requestIdMock = 1;
//        long handymanIdMock = 1;
//        String commentMock = "commentMock";
//        RequestAssignmentPayload payload = new RequestAssignmentPayload(requestIdMock, handymanIdMock, commentMock);
//        Request request = mock(Request.class);
//
//        RequestAssignment result = assertDoesNotThrow(() -> target.create(request, payload));
//
//        assertEquals(request, result.getRequest());
//        assertEquals(handymanIdMock, result.getHandymanId());
//        assertEquals(commentMock, result.getComment());
//        assertNull(result.getId()); // ещё не сохранён
//    }
//
//    @Test
//    void read__MapsEntityToDto() {
//        long assignmentIdMock = 1;
//        long requestIdMock = 2;
//        long handymanIdMock = 1;
//        AssignmentAction actionMock = mock(AssignmentAction.class);
//        LocalDateTime timeMock = LocalDateTime.now();
//        Request request = Request.builder().id(requestIdMock).build();
//        String commentMock = "commentMock";
//        RequestAssignment entityMock = RequestAssignment.builder()
//                .id(assignmentIdMock)
//                .request(request)
//                .handymanId(handymanIdMock)
//                .action(actionMock)
//                .processedAt(timeMock)
//                .createdAt(timeMock)
//                .updatedAt(timeMock)
//                .comment(commentMock)
//                .build();
//
//        RequestAssignmentDto result = assertDoesNotThrow(() -> target.read(entityMock));;
//
//        assertEquals(assignmentIdMock, result.id());
//        assertEquals(requestIdMock, result.requestId());
//        assertEquals(handymanIdMock, result.handymanId());
//        assertEquals(actionMock, result.action());
//        assertEquals(timeMock, result.processedAt());
//        assertEquals(timeMock, result.createdAt());
//        assertEquals(timeMock, result.updatedAt());
//        assertEquals(commentMock, result.comment());
//    }
//
//    @Test
//    void readPage__MapsPageOfAssignments() {
//        Request requestMock = Request.builder().id(10L).build();
//        long assignmentIdMock = 1;
//        RequestAssignment assignmentMock = RequestAssignment.builder()
//                .id(assignmentIdMock)
//                .request(requestMock)
//                .build();
//        Page<RequestAssignment> pageMock = new PageImpl<>(List.of(assignmentMock));
//
//        PageDto<RequestAssignmentDto> result = assertDoesNotThrow(() -> target.readPage(pageMock));
//
//        assertEquals(0, result.page());
//        assertEquals(1, result.size());
//        assertEquals(1, result.total());
//        assertFalse(result.hasNext());
//        assertFalse(result.hasPrev());
//        assertEquals(1, result.content().size());
//        assertEquals(assignmentIdMock, result.content().getFirst().id());
//    }
//
//    @Test
//    void update__UpdatesNonNullFields() {
//        AssignmentAction oldActionMock = mock(AssignmentAction.class);
//        long newHandymanMock = 2;
//        String newCommentMock = "newCommentMock";
//        RequestAssignment entityMock = RequestAssignment.builder()
//                .id(1L)
//                .handymanId(1)
//                .action(oldActionMock)
//                .comment("oldCommentMock")
//                .build();
//        RequestAssignmentUpdatePayload payloadMock = new RequestAssignmentUpdatePayload(action, newHandymanMock, newCommentMock);
//
//        when(actionMapper.map(entityMock)).thenReturn(entityMock);
//
//        RequestAssignment result = assertDoesNotThrow(() -> target.update(entityMock, payloadMock));
//
//        assertEquals(newHandymanMock, result.getHandymanId());
//        assertEquals(newCommentMock, result.getComment());
//    }
//
//    @Test
//    void update__SkipsNullFields() {
//        AssignmentAction actionMock = mock(AssignmentAction.class);
//        String oldComment = "oldComment";
//        RequestAssignment assignment = RequestAssignment.builder()
//                .handymanId(1)
//                .action(actionMock)
//                .comment(oldComment)
//                .build();
//
//        RequestAssignmentUpdatePayload payload = new RequestAssignmentUpdatePayload(null, null, null);
//
//        RequestAssignment updated = target.update(assignment, payload);
//
//        assertEquals(assignment.getHandymanId(), updated.getHandymanId());
//        assertEquals(actionMock, updated.getAction());
//        assertEquals(oldComment, updated.getComment());
//    }
//}